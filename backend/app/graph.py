from langgraph.graph import StateGraph
from langgraph.graph import START
from langgraph.graph import END

from app.state import State
from app.chatbot import chatbot

builder = StateGraph(State)

builder.add_node("chatbot", chatbot)

builder.add_edge(START, "chatbot")

builder.add_edge("chatbot", END)

graph = builder.compile()
