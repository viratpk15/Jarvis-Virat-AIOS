from typing import TypedDict, Any


class State(TypedDict):
    session_id: str

    message: str

    action: dict[str, Any]

    observation: dict[str, Any]

    response: str

    iteration_count: int
