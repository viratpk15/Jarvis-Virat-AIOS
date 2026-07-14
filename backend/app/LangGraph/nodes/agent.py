import json

from langchain_core.messages import HumanMessage

from app.LLM.client import llm
from app.Prompts.agent import AGENT_PROMPT

from app.LangGraph.state import State


def agent(state: State):
    """Call the LLM, parse the response as a JSON action, and update state.

    If the LLM response is not valid JSON, it is treated as a final
    response. If the parsed action is missing the required 'type' key,
    it is also treated as a final response with the raw LLM output.

    Args:
        state: The current LangGraph state.

    Returns:
        A state update dict containing the parsed action and optional response.
    """
    prompt = f"""
{AGENT_PROMPT}

User:

{state["message"]}

Observation:

{json.dumps(state["observation"])}
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    try:
        action = json.loads(response.content)

    except json.JSONDecodeError:
        action = {
            "type": "final",
            "response": response.content,
        }

    # Guard against missing or non-dict action from the LLM
    if not isinstance(action, dict):
        action = {
            "type": "final",
            "response": response.content,
        }

    action_type = action.get("type")

    if action_type == "final":
        return {
            "action": action,
            "response": action.get("response", response.content),
        }

    if action_type == "tool":
        return {
            "action": action,
        }

    # Unknown action type - treat as final response
    return {
        "action": {"type": "final", "response": response.content},
        "response": response.content,
    }
