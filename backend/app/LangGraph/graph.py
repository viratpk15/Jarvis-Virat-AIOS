from langgraph.graph import StateGraph, START, END

from app.LangGraph.state import State

from app.LangGraph.nodes.agent import agent
from app.LangGraph.nodes.tool_node import tool_node

# Maximum number of tool-calling iterations before forcing a final response.
# Prevents infinite loops when the LLM repeatedly requests tool execution.
MAX_TOOL_ITERATIONS = 10

builder = StateGraph(State)

builder.add_node("agent", agent)
builder.add_node("tool", tool_node)


def route(state: State):
    """Route to the tool node or end execution.

    If the action type is 'tool', route to the tool node.
    If the iteration count exceeds the maximum, force a final response
    to prevent infinite loops.

    Args:
        state: The current LangGraph state.

    Returns:
        The next node name ('tool' or END).
    """
    if state["action"].get("type") == "tool":
        iteration_count = state.get("iteration_count", 0)
        if iteration_count >= MAX_TOOL_ITERATIONS:
            return END
        return "tool"

    return END


builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    route,
    {
        "tool": "tool",
        END: END,
    },
)

builder.add_edge("tool", "agent")

graph = builder.compile()
