"""
Jarvis AIOS
-----------
FastAPI Response Schemas

Standardised Pydantic response models for all API endpoints.
All endpoints should return these models for consistent frontend integration.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """A single error detail item.

    Used inside ErrorResponse to provide structured error information
    that can be rendered by the frontend.

    Attributes:
        code: Machine-readable error code (e.g. "invalid_credentials").
        message: Human-readable error description.
        details: Optional additional context (e.g. validation errors).
    """

    code: str = Field(
        ...,
        description="Machine-readable error code for programmatic handling.",
        examples=["invalid_credentials", "session_forbidden", "validation_error"],
    )
    message: str = Field(
        ...,
        description="Human-readable error description.",
        examples=["Invalid or expired token"],
    )
    details: dict[str, Any] | None = Field(
        default=None,
        description="Optional additional context (e.g. field-level validation errors).",
        examples=[{"field": "email", "reason": "already registered"}],
    )


class ErrorResponse(BaseModel):
    """Standard error response for all API endpoints.

    Every HTTP error response should conform to this schema
    so the frontend can handle errors uniformly.

    Attributes:
        error: The structured error information.
    """

    error: ErrorDetail = Field(
        ...,
        description="Structured error information with code, message, and optional details.",
    )


class ChatResponse(BaseModel):
    """Response model for the chat endpoint.

    Attributes:
        response: The AI-generated response text.
    """

    response: str = Field(
        ...,
        description="The AI assistant's response to the user's message.",
        examples=["The weather today is sunny with a high of 25°C."],
    )


class HealthResponse(BaseModel):
    """Response model for the health check endpoint.

    Attributes:
        status: Service health status.
        version: Running version of the application.
    """

    status: str = Field(
        ...,
        description="Service health status.",
        examples=["ok"],
    )
    version: str = Field(
        ...,
        description="Running version of the application.",
        examples=["1.0.0"],
    )