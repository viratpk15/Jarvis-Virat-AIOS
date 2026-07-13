from app.LangGraph.state import State
from app.Tools.engine import engine


def tool_node(state: State):

    if not state["need_tool"]:
        return {}

    result = engine.execute(state["tool_name"], **state["tool_args"])

    return {"tool_result": result}
