"""
Jarvis Runtime
"""

from app.LangGraph.graph import graph


class Jarvis:
    def chat(
        self,
        session_id: str,
        message: str,
    ) -> str:

        result = graph.invoke(
            {
                "session_id": session_id,
                "message": message,
                "action": {},
                "observation": {},
                "response": "",
                "iteration_count": 0,
            }
        )

        return result["response"]


jarvis = Jarvis()
