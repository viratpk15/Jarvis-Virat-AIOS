import json

from langchain_core.messages import HumanMessage

from app.LLM.client import llm
from app.Prompts.agent import AGENT_PROMPT

from app.LangGraph.state import State


def agent(state: State):

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

    except Exception:
        action = {
            "type": "final",
            "response": response.content,
        }

    if action["type"] == "final":
        return {
            "action": action,
            "response": action["response"],
        }

    return {
        "action": action,
    }
