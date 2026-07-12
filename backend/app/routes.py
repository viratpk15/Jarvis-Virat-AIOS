from fastapi import APIRouter

from app.models import ChatRequest, ChatResponse
from app.chatbot import chat

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat_route(request: ChatRequest):

    answer = chat(request.message)

    return ChatResponse(response=answer)
