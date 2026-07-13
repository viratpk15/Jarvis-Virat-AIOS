from langgraph.graph import StateGraph
from langgraph.graph import START, END

from app.LangGraph.state import State
from app.LangGraph.nodes.chatbot import chatbot

builder = StateGraph(State)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()
