from app.LangGraph.state import State

from app.Tools.engine import engine


def tool_node(state: State):

    action = state["action"]

    result = engine.execute(
        action["tool"],
        **action.get("arguments", {}),
    )

    return {
        "observation": {
            "result": result,
        }
    }
