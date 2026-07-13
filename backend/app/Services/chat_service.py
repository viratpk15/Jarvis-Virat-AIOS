from app.LangGraph.graph import graph


def chat(session_id: str, message: str):

    result = graph.invoke(
        {
            "session_id": session_id,
            "message": message,
            "response": "",
        }
    )

    return result["response"]
