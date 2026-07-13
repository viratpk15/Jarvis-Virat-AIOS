from typing import TypedDict, Any


class State(TypedDict):
    session_id: str
    message: str

    need_tool: bool
    tool_name: str
    tool_args: dict[str, Any]
    tool_result: Any

    response: str
