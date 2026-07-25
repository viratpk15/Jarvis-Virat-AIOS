from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
import uuid
import sqlite3
from pathlib import Path

from app.Auth.dependencies import get_current_user
from app.Auth.models import User
from app.Config.settings import PERSISTENCE_DB_PATH
from app.FastAPI.schemas import ConversationSummary, ErrorResponse

router = APIRouter()


def _db_connection() -> sqlite3.Connection:
    db_path = PERSISTENCE_DB_PATH
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)


def _ensure_tables(conn: sqlite3.Connection) -> None:
    """Ensure the sessions table has the required columns."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            user_id INTEGER,
            title TEXT DEFAULT 'New Conversation',
            pinned INTEGER DEFAULT 0,
            summary TEXT,
            created_at TEXT NOT NULL,
            last_accessed TEXT NOT NULL
        )
    """)
    # Add title column if missing (for databases created before schema update)
    try:
        cursor.execute("ALTER TABLE sessions ADD COLUMN title TEXT DEFAULT 'New Conversation'")
    except sqlite3.OperationalError:
        pass  # Column already exists
    # Add pinned column if missing
    try:
        cursor.execute("ALTER TABLE sessions ADD COLUMN pinned INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass  # Column already exists
    conn.commit()


def _build_summary(row) -> ConversationSummary:
    """Build a ConversationSummary from a database row."""
    return ConversationSummary(
        id=row[0],
        title=row[1] if row[1] else "Conversation",
        preview="",
        time="",
        pinned=bool(row[2]) if row[2] else False,
        model="Gemini 2.5 Pro",
        unread=False,
        group="Today",
    )


class RenameRequest(BaseModel):
    title: str = Field(..., description="New conversation title")


class PinRequest(BaseModel):
    pinned: bool = Field(..., description="Pinned status")


@router.get("/conversations", response_model=List[ConversationSummary], tags=["conversations"], summary="List conversations")
async def list_conversations(current_user: User = Depends(get_current_user)):
    with _db_connection() as conn:
        _ensure_tables(conn)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT session_id, title, pinned FROM sessions WHERE user_id = ? ORDER BY pinned DESC, last_accessed DESC",
            (current_user.id,),
        )
        rows = cursor.fetchall()
    return [_build_summary(row) for row in rows]


@router.post("/conversations", response_model=ConversationSummary, status_code=status.HTTP_201_CREATED, tags=["conversations"], summary="Create a new conversation")
async def create_conversation(current_user: User = Depends(get_current_user)):
    session_id = f"ses_{uuid.uuid4().hex[:12]}"
    with _db_connection() as conn:
        _ensure_tables(conn)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sessions (session_id, user_id, title, pinned, created_at, last_accessed) VALUES (?, ?, ?, 0, datetime('now'), datetime('now'))",
            (session_id, current_user.id, "New Conversation"),
        )
        conn.commit()
    return ConversationSummary(
        id=session_id,
        title="New Conversation",
        preview="",
        time="Just now",
        pinned=False,
        model="Gemini 2.5 Pro",
        unread=False,
        group="Today",
    )


@router.delete("/conversations/{session_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["conversations"], summary="Delete a conversation")
async def delete_conversation(session_id: str, current_user: User = Depends(get_current_user)):
    with _db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": {"code": "not_found", "message": "Conversation not found"}})
        if row[0] != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"error": {"code": "session_forbidden", "message": "Session does not belong to the authenticated user"}})
        # Delete messages first (foreign key constraint)
        cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
        conn.commit()
    return None


@router.patch("/conversations/{session_id}/rename", response_model=ConversationSummary, tags=["conversations"], summary="Rename a conversation")
async def rename_conversation(session_id: str, req: RenameRequest, current_user: User = Depends(get_current_user)):
    with _db_connection() as conn:
        _ensure_tables(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": {"code": "not_found", "message": "Conversation not found"}})
        if row[0] != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"error": {"code": "session_forbidden", "message": "Session does not belong to the authenticated user"}})
        # Persist the new title
        cursor.execute(
            "UPDATE sessions SET title = ?, last_accessed = datetime('now') WHERE session_id = ?",
            (req.title, session_id),
        )
        conn.commit()
        # Read back the updated row
        cursor.execute(
            "SELECT session_id, title, pinned FROM sessions WHERE session_id = ?",
            (session_id,),
        )
        updated_row = cursor.fetchone()
    return _build_summary(updated_row)


@router.post("/conversations/{session_id}/pin", response_model=ConversationSummary, tags=["conversations"], summary="Toggle pin status")
async def pin_conversation(session_id: str, req: PinRequest, current_user: User = Depends(get_current_user)):
    with _db_connection() as conn:
        _ensure_tables(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": {"code": "not_found", "message": "Conversation not found"}})
        if row[0] != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"error": {"code": "session_forbidden", "message": "Session does not belong to the authenticated user"}})
        # Persist the pinned status
        cursor.execute(
            "UPDATE sessions SET pinned = ?, last_accessed = datetime('now') WHERE session_id = ?",
            (1 if req.pinned else 0, session_id),
        )
        conn.commit()
        # Read back the updated row
        cursor.execute(
            "SELECT session_id, title, pinned FROM sessions WHERE session_id = ?",
            (session_id,),
        )
        updated_row = cursor.fetchone()
    return _build_summary(updated_row)