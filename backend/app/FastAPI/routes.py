"""
Jarvis AIOS
-----------
FastAPI Routes

HTTP endpoints for the chat functionality.
All chat endpoints require authentication.

Every endpoint returns standardised Pydantic response models.
Error responses follow the ErrorResponse schema for consistent
frontend error handling.

POST /chat  — generous rate limit (30/minute)
"""

from fastapi import APIRouter, Depends, Request, status

from app.FastAPI.request_models import ChatRequest
from app.FastAPI.schemas import ChatResponse, ErrorResponse, HealthResponse
from app.Services.chat_service import chat
from app.Auth.dependencies import get_current_user
from app.Auth.models import User
from app.FastAPI.dependencies import verify_session_ownership
from app.FastAPI.rate_limiter import limiter
from app.Config.settings import CHAT_RATE_LIMIT

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description=(
        "Returns the current health status and running version "
        "of the Jarvis AIOS backend."
    ),
    responses={
        status.HTTP_200_OK: {
            "description": "Service is healthy and running.",
            "model": HealthResponse,
        },
    },
)
def health_check() -> HealthResponse:
    """Perform a health check on the service.

    Returns:
        HealthResponse with status "ok" and the current version.
    """
    return HealthResponse(status="ok", version="1.0.0")


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Send a Chat Message",
    description=(
        "Process a chat message within an authenticated session. "
        "The session_id is bound to the authenticated user. If the session "
        "does not exist, it is created. If it exists but belongs to another "
        "user, a 403 Forbidden is returned."
    ),
    responses={
        status.HTTP_200_OK: {
            "description": "Chat response generated successfully.",
            "model": ChatResponse,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing or invalid authentication token.",
            "model": ErrorResponse,
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Session does not belong to the authenticated user.",
            "model": ErrorResponse,
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            "description": "Rate limit exceeded. Too many chat requests.",
            "model": ErrorResponse,
        },
    },
)
@limiter.limit(CHAT_RATE_LIMIT)
def chat_route(
    request: Request,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
) -> ChatResponse:
    """Process a chat message within an authenticated session.

    The session_id is bound to the authenticated user. If the session
    does not exist, it is created. If it exists but belongs to another
    user, a 403 Forbidden is returned.

    Args:
        request: The incoming request (required by slowapi).
        chat_request: The chat request containing session_id and message.
        current_user: The authenticated user from JWT token.

    Returns:
        The chat response containing the AI-generated answer.

    Raises:
        HTTPException: 403 if session ownership is violated.
    """
    # Verify session ownership before processing
    verify_session_ownership(session_id=chat_request.session_id, current_user=current_user)

    answer = chat(
        session_id=chat_request.session_id,
        message=chat_request.message,
    )

    return ChatResponse(response=answer)