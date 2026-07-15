"""
Jarvis AIOS
-----------
Main Application Entry Point

Creates the FastAPI application with comprehensive OpenAPI metadata
and includes all routers. Applies rate limiting and global exception handlers.

The Runtime is the only public entry point into Jarvis.
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from slowapi.errors import RateLimitExceeded

from app.FastAPI.routes import router as chat_router
from app.Auth.routes import router as auth_router
from app.Config.settings import APP_VERSION
from app.FastAPI.rate_limiter import limiter

app = FastAPI(
    title="Jarvis AIOS",
    description=(
        "Jarvis AI Operating System — a production-grade backend "
        "for conversational AI with memory, tool execution, "
        "observability, and authentication."
    ),
    version=APP_VERSION,
    summary="AI Operating System backend API",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Jarvis AIOS Team",
        "url": "https://github.com/Viratpk/Jarvis-Virat-AIOS",
    },
    license_info={
        "name": "MIT",
    },
)


# ---------------------------------------------------------------------------
# Rate limiting middleware
# ---------------------------------------------------------------------------

app.state.limiter = limiter


# ---------------------------------------------------------------------------
# Global exception handlers
# ---------------------------------------------------------------------------


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(
    request: Request,
    exc: RateLimitExceeded,
) -> JSONResponse:
    """Return standardised ErrorResponse on rate limit violation (HTTP 429).

    Returns:
        JSON with error code ``rate_limited`` and a human-readable message.
        The ``Retry-After`` header is set by slowapi automatically.
    """
    return JSONResponse(
        status_code=429,
        content={
            "error": {
                "code": "rate_limited",
                "message": "Too many requests. Please slow down.",
            }
        },
        headers=getattr(exc, "headers", None),
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    """Convert all HTTP exceptions to the standardised ErrorResponse schema.

    If the exception detail is already a dict matching the ErrorResponse
    structure, it is passed through. Otherwise it is wrapped into a
    generic error response.
    """
    detail = exc.detail
    if isinstance(detail, dict) and "error" in detail:
        # Already structured — pass through
        return JSONResponse(
            status_code=exc.status_code,
            content=detail,
            headers=getattr(exc, "headers", None),
        )

    # Fallback: wrap the plain string detail
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "http_error",
                "message": str(detail),
            }
        },
        headers=getattr(exc, "headers", None),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Convert Pydantic validation errors to the standardised ErrorResponse.

    Returns a 422 with field-level details to help frontend debugging.
    """
    errors = exc.errors()
    field_errors = {}
    for err in errors:
        loc = " -> ".join(str(loc_part) for loc_part in err.get("loc", []))
        field_errors[loc] = err.get("msg", "Unknown validation error")

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "validation_error",
                "message": "Request validation failed",
                "details": field_errors,
            }
        },
    )


# ---------------------------------------------------------------------------
# Include routers
# ---------------------------------------------------------------------------

# Auth endpoints (public)
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Chat endpoints (protected)
app.include_router(chat_router, tags=["chat"])