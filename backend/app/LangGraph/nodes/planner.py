import re

from app.LangGraph.state import State


def planner(state: State):

    message = state["message"]

    decision = {"need_tool": False, "tool_name": "", "tool_args": {}}

    expression = re.search(r"(\d+[\+\-\*\/]\d+)", message.replace(" ", ""))

    if expression:
        decision["need_tool"] = True
        decision["tool_name"] = "calculator"
        decision["tool_args"] = {"expression": expression.group(1)}

    return decision
