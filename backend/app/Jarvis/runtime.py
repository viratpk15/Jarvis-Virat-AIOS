"""
Jarvis Runtime

Public entry point for Jarvis AIOS. Constructs the initial LangGraph state
and invokes the graph. Wraps each request in an execution trace so that
every request produces a complete, developer-friendly trace (observability).
Tracing is fully optional: if tracing fails, the request proceeds normally.
"""

import json
import logging
import time
from typing import Generator

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.LangGraph.graph import graph
from app.LLM.client import llm_client
from app.Memory.manager import memory_manager
from app.Observability.manager import observability_manager
from app.Observability.trace import calculate_duration, measure_time, trace_context
from app.Prompts.agent import AGENT_PROMPT

logger = logging.getLogger(__name__)

# Maximum number of characters of the user request stored in a trace.
_MAX_TRACED_REQUEST_LENGTH: int = 500


def _format_sse(event_type: str, data: dict) -> str:
    """Format structured Server-Sent Events (SSE) frame.

    Args:
        event_type: Event type (thinking, token, done, error).
        data: Payload dict to encode as JSON.

    Returns:
        Formatted SSE text chunk.
    """
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"


class Jarvis:
    def chat(
        self,
        session_id: str,
        message: str,
    ) -> str:
        # Wrap the entire request in a trace. The trace is optional and
        # never affects execution: failures inside tracing are swallowed.
        with trace_context(
            session_id,
            message[:_MAX_TRACED_REQUEST_LENGTH],
        ):
            result = graph.invoke(
                {
                    "session_id": session_id,
                    "message": message,
                    "action": {},
                    "observation": {},
                    "response": "",
                    "iteration_count": 0,
                    "plan": {},
                    "request_type": "conversation",
                    "execution_outcome": None,
                    "execution_start_time": time.perf_counter(),
                    "replanning_count": 0,
                    "tool_retry_count": 0,
                    "consecutive_failures": 0,
                    "step_execution_history": [],
                    "termination_reason": None,
                }
            )

        return result["response"]

    def chat_stream(
        self,
        session_id: str,
        message: str,
    ) -> Generator[str, None, None]:
        """Stream chat tokens in real-time using provider-independent LLMClient and structured SSE.

        Emits structured SSE events:
          - event: thinking
          - event: token
          - event: done
          - event: error

        Persists the final assistant message to SQLite ONLY when generation completes successfully.

        Args:
            session_id: Unique session identifier.
            message: User prompt text.

        Yields:
            Structured SSE event frame strings.
        """
        start_time = measure_time()

        with trace_context(
            session_id,
            message[:_MAX_TRACED_REQUEST_LENGTH],
        ):
            # 1. Emit thinking event immediately
            yield _format_sse("thinking", {"status": "Thinking..."})

            # 2. Memory & semantic retrieval
            memory = memory_manager.get_conversation(session_id)
            mem_start = measure_time()
            relevant_memories = memory_manager.get_relevant_memories(
                session_id=session_id,
                query=message,
                top_k=5,
            )
            mem_duration = calculate_duration(mem_start)

            summary_used = bool(
                memory.messages
                and memory.messages[0].__class__.__name__ == "SystemMessage"
                and "Conversation Summary:" in memory.messages[0].content
            )
            observability_manager.record_memory_info(
                conversation_messages=len(memory.messages),
                summary_used=summary_used,
                semantic_memories=len(relevant_memories),
                retrieval_latency_ms=mem_duration,
            )

            # 3. Assemble system and context messages
            messages: list = [SystemMessage(content=AGENT_PROMPT)]
            messages.extend(memory.messages)

            if relevant_memories:
                memories_text = "Relevant Memories:\n" + "\n".join(
                    f"- {m.content}" for m in relevant_memories
                )
                messages.append(SystemMessage(content=memories_text))

            user_msg = HumanMessage(content=message)
            messages.append(user_msg)

            # Save user message to memory & SQLite persistence
            memory.add_message(user_msg)

            accumulated_tokens: list[str] = []

            try:
                # 4. Stream tokens via provider-independent LLMClient abstraction
                for token in llm_client.stream(messages):
                    accumulated_tokens.append(token)
                    yield _format_sse("token", {"token": token})

                full_response = "".join(accumulated_tokens)

                # 5. Persist final assistant message ONLY upon successful completion
                memory.add_message(AIMessage(content=full_response))

                # Record LLM usage metrics
                observability_manager.record_llm_usage(
                    model_name=getattr(llm_client.provider, "model", "") or "",
                    latency_ms=calculate_duration(start_time),
                )

                # 6. Emit done event
                yield _format_sse("done", {"response": full_response})

            except Exception as exc:
                logger.error("Inference exception during streaming for session %s: %s", session_id, str(exc))
                yield _format_sse("error", {"error": str(exc)})
                raise


jarvis = Jarvis()

