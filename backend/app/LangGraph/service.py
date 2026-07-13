from app.LangGraph.graph import graph


def chat(message: str) -> str:

    result = graph.invoke(
        {
            "message": message,
            "response": "",
        }
    )

    return result["response"]
