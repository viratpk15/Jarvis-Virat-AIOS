"""
Jarvis Runtime

Public entry point for Jarvis AIOS. Constructs the initial LangGraph state
and invokes the graph. Wraps each request in an execution trace so that
every request produces a complete, developer-friendly trace (observability).
Tracing is fully optional: if tracing fails, the request proceeds normally.
"""

import time

from app.LangGraph.graph import graph
from app.Observability.trace import trace_context

# Maximum number of characters of the user request stored in a trace.
_MAX_TRACED_REQUEST_LENGTH: int = 500


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


jarvis = Jarvis()
