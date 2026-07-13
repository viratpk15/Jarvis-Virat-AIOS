from typing import TypedDict


class State(TypedDict):
    session_id: str
    message: str
    response: str
