from langgraph.graph import StateGraph, START, END

from app.LangGraph.state import State

from app.LangGraph.nodes.agent import agent
from app.LangGraph.nodes.tool_node import tool_node

builder = StateGraph(State)

builder.add_node("agent", agent)
builder.add_node("tool", tool_node)


def route(state: State):

    if state["action"].get("type") == "tool":
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
