from langgraph.graph import StateGraph
from langgraph.graph import START, END

from app.LangGraph.state import State

from app.LangGraph.nodes.planner import planner
from app.LangGraph.nodes.tool_node import tool_node
from app.LangGraph.nodes.chatbot import chatbot

builder = StateGraph(State)


builder.add_node("planner", planner)
builder.add_node("tool", tool_node)
builder.add_node("chatbot", chatbot)


def router(state: State):

    if state["need_tool"]:
        return "tool"

    return "chatbot"


builder.add_edge(START, "planner")

builder.add_conditional_edges(
    "planner",
    router,
    {
        "tool": "tool",
        "chatbot": "chatbot",
    },
)

builder.add_edge("tool", "chatbot")

builder.add_edge("chatbot", END)

graph = builder.compile()
