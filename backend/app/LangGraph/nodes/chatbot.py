import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

from app.Memory.conversation import memory

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
)


def chatbot(state):

    # Store user message
    memory.add_message(HumanMessage(content=state["message"]))

    # Send complete conversation
    response = llm.invoke(memory.messages)

    # Store AI response
    memory.add_message(AIMessage(content=response.content))

    return {"response": response.content}
