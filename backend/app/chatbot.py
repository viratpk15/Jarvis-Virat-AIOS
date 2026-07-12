import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
)


def chatbot(state):

    response = llm.invoke(state["message"])

    return {"response": response.content}


def chat(message: str):

    result = graph.invoke(
        {
            "message": message,
            "response": "",
        }
    )

    return result["response"]


from app.graph import graph
