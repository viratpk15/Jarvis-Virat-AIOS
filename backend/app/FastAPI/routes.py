from fastapi import APIRouter

from app.FastAPI.request_models import ChatRequest, ChatResponse
from app.LangGraph.service import chat

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat_route(request: ChatRequest):

    answer = chat(
        session_id=request.session_id,
        message=request.message,
    )

    return ChatResponse(response=answer)
