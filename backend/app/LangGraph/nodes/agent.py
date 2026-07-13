import json

from langchain_core.messages import HumanMessage

from app.LLM.client import llm
from app.Prompts.agent import AGENT_PROMPT

from app.LangGraph.state import State


def agent(state: State):

    response = llm.invoke(
        [
            HumanMessage(
                content=f"""
{AGENT_PROMPT}

User:

{state["message"]}
"""
            )
        ]
    )

    try:
        decision = json.loads(response.content)

    except Exception:
        decision = {
            "type": "final",
            "response": response.content,
        }

    return decision
