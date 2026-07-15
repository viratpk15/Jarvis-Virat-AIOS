"""
Jarvis AIOS
-----------
FastAPI Dependencies

Reusable FastAPI dependencies for endpoint protection and validation.
These dependencies are injected via Depends() into route handlers.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from fastapi import Depends, HTTPException, status

from app.Auth.dependencies import get_current_user
from app.Auth.models import User
from app.Config.settings import PERSISTENCE_DB_PATH


def verify_session_ownership(
    session_id: str,
    current_user: User = Depends(get_current_user),
) -> User:
    """Verify that a chat session belongs to the authenticated user.

    Chat sessions are bound to the authenticated user who created them.
    If the session does not yet exist, it is considered owned by the
    requesting user (creation-on-demand). If it exists but is bound to
    a different user, a 403 Forbidden is raised.

    Args:
        session_id: The chat session identifier to verify.
        current_user: The authenticated user from JWT token.

    Returns:
        The authenticated User if ownership is confirmed.

    Raises:
        HTTPException: 403 if the session belongs to a different user.
    """
    db_path = PERSISTENCE_DB_PATH
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id FROM sessions WHERE session_id = ?",
            (session_id,),
        )
        row = cursor.fetchone()

    if row is not None and row[0] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "code": "session_forbidden",
                    "message": "Session does not belong to the authenticated user",
                }
            },
        )

    return current_user