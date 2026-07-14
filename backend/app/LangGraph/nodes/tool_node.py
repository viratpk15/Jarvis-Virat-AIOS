from app.LangGraph.state import State

from app.Tools.engine import engine


def tool_node(state: State):
    """Execute the tool specified in the current action.

    Catches execution errors and returns them as observations so the
    agent can decide how to respond instead of crashing the request.

    Args:
        state: The current LangGraph state containing the action dict.

    Returns:
        A state update dict with the observation populated.
    """
    action = state["action"]

    # Increment the iteration counter so the graph can enforce the recursion limit
    iteration_count = state.get("iteration_count", 0) + 1

    try:
        result = engine.execute(
            action["tool"],
            **action.get("arguments", {}),
        )
    except ValueError as e:
        return {
            "iteration_count": iteration_count,
            "observation": {
                "error": str(e),
            },
        }

    return {
        "iteration_count": iteration_count,
        "observation": {
            "result": result,
        },
    }
