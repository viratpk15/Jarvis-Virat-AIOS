from app.LangGraph.state import State

from app.Tools.engine import engine


def tool_node(state: State):
    """Execute the tool specified in the current action.

    Catches execution errors and returns them as observations so the
    agent can decide how to respond instead of crashing the request.
    Marks the current plan step as completed after successful execution.

    Args:
        state: The current LangGraph state containing the action dict.

    Returns:
        A state update dict with the observation populated and plan updated.
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
        # Mark current step as failed
        updated_plan = state.get("plan", {})
        if updated_plan:
            for step in updated_plan.get("steps", []):
                if step.get("status") == "in_progress":
                    step["status"] = "failed"
                    break

        return {
            "iteration_count": iteration_count,
            "observation": {
                "error": str(e),
            },
            "plan": updated_plan,
        }

    # Mark current step as completed
    updated_plan = state.get("plan", {})
    if updated_plan:
        for step in updated_plan.get("steps", []):
            if step.get("status") == "in_progress":
                step["status"] = "completed"
                break

    return {
        "iteration_count": iteration_count,
        "observation": {
            "result": result,
        },
        "plan": updated_plan,
    }
