"""
SQLite Persistence Backend

Provides SQLite-backed persistent storage for conversation history and summaries.
All SQL operations use parameterized queries to prevent SQL injection.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage


class SQLitePersistenceBackend:
    """SQLite-backed persistent storage for memory.

    Stores conversation history, summaries, and session metadata in SQLite.
    All SQL operations use parameterized queries to prevent SQL injection.
    Tables are created automatically on initialization.

    Attributes:
        db_path: Path to SQLite database file.
    """

    def __init__(self, db_path: str = "./data/memory.db"):
        """Initialize SQLite persistence backend.

        Args:
            db_path: Path to SQLite database file.
                Defaults to "./data/memory.db".
        """
        self.db_path = db_path
        self._ensure_tables_exist()

    def _get_connection(self) -> sqlite3.Connection:
        """Get SQLite database connection.

        Returns:
            SQLite connection object.
        """
        # Ensure directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(self.db_path)

    def _ensure_tables_exist(self) -> None:
        """Create database tables if they don't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Sessions table (user_id binds sessions to authenticated users)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    summary TEXT,
                    created_at TEXT NOT NULL,
                    last_accessed TEXT NOT NULL
                )
            """)

            # Messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    message_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    order_in_session INTEGER NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            """)

            # Create index for efficient session queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_session
                ON messages(session_id, order_in_session)
            """)

            # Create table for message embeddings
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS message_embeddings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    position INTEGER NOT NULL,
                    embedding BLOB NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            """)

            # Create index for embedding queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_embeddings_session
                ON message_embeddings(session_id, position)
            """)

            # Create table for summary embeddings
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS summary_embeddings (
                    session_id TEXT PRIMARY KEY,
                    embedding BLOB NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            """)

            # Create table for execution state
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS execution_state (
                    session_id TEXT PRIMARY KEY,
                    current_plan TEXT,
                    current_step INTEGER,
                    completed_steps TEXT NOT NULL,
                    pending_steps TEXT NOT NULL,
                    execution_status TEXT NOT NULL DEFAULT 'idle',
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            """)

            conn.commit()

    def load_session(self, session_id: str) -> dict[str, Any] | None:
        """Load session data from SQLite.

        Args:
            session_id: Unique session identifier.

        Returns:
            Dict containing 'summary' and 'messages', or None if session not found.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Load session metadata
            cursor.execute(
                "SELECT summary FROM sessions WHERE session_id = ?",
                (session_id,)
            )
            row = cursor.fetchone()

            if not row:
                return None

            summary = row[0]

            # Load messages
            cursor.execute(
                "SELECT message_type, content, timestamp FROM messages "
                "WHERE session_id = ? ORDER BY order_in_session ASC",
                (session_id,)
            )
            message_rows = cursor.fetchall()

            # Convert to LangChain message format
            messages = []
            for msg_type, content, timestamp in message_rows:
                if msg_type == "human":
                    messages.append(HumanMessage(content=content))
                elif msg_type == "ai":
                    messages.append(AIMessage(content=content))
                elif msg_type == "system":
                    messages.append(SystemMessage(content=content))

            return {
                "summary": summary,
                "messages": messages,
            }

    def load_summary(self, session_id: str) -> str | None:
        """Load only the summary for a session.

        Args:
            session_id: Unique session identifier.

        Returns:
            Summary text, or None if not found.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT summary FROM sessions WHERE session_id = ?",
                (session_id,)
            )
            row = cursor.fetchone()
            return row[0] if row else None

    def append_message(self, session_id: str, message: BaseMessage, position: int) -> None:
        """Append a single new message to SQLite.

        Args:
            session_id: Unique session identifier.
            message: Message to append.
            position: Message position in session (0-indexed).
        """
        now = datetime.utcnow().isoformat()
        msg_type = self._get_message_type(message)

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Ensure session exists
            cursor.execute(
                """
                INSERT OR IGNORE INTO sessions (session_id, summary, created_at, last_accessed)
                VALUES (?, ?, ?, ?)
                """,
                (session_id, None, now, now)
            )

            # Insert the new message
            cursor.execute(
                """
                INSERT INTO messages (session_id, message_type, content, timestamp, order_in_session)
                VALUES (?, ?, ?, ?, ?)
                """,
                (session_id, msg_type, message.content, now, position)
            )

            # Update last_accessed
            cursor.execute(
                "UPDATE sessions SET last_accessed = ? WHERE session_id = ?",
                (now, session_id)
            )

            conn.commit()

    def update_summary(self, session_id: str, summary: str) -> None:
        """Update only the summary for a session.

        Args:
            session_id: Unique session identifier.
            summary: New summary text.
        """
        now = datetime.utcnow().isoformat()

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Ensure session exists
            cursor.execute(
                """
                INSERT OR IGNORE INTO sessions (session_id, summary, created_at, last_accessed)
                VALUES (?, ?, ?, ?)
                """,
                (session_id, summary, now, now)
            )

            # Update summary
            cursor.execute(
                "UPDATE sessions SET summary = ?, last_accessed = ? WHERE session_id = ?",
                (summary, now, session_id)
            )

            conn.commit()

    def replace_message_window(self, session_id: str, messages: list[BaseMessage]) -> None:
        """Replace all messages for a session with a new window.

        Used after summarization to persist the trimmed message window.

        Args:
            session_id: Unique session identifier.
            messages: New message window to persist.
        """
        now = datetime.utcnow().isoformat()

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Delete existing messages
            cursor.execute(
                "DELETE FROM messages WHERE session_id = ?",
                (session_id,)
            )

            # Insert new message window
            for idx, msg in enumerate(messages):
                msg_type = self._get_message_type(msg)
                cursor.execute(
                    """
                    INSERT INTO messages (session_id, message_type, content, timestamp, order_in_session)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (session_id, msg_type, msg.content, now, idx)
                )

            # Update last_accessed
            cursor.execute(
                "UPDATE sessions SET last_accessed = ? WHERE session_id = ?",
                (now, session_id)
            )

            conn.commit()

    def delete_session(self, session_id: str) -> None:
        """Delete session and all its messages from SQLite.

        Args:
            session_id: Unique session identifier.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Delete messages first (foreign key constraint)
            cursor.execute(
                "DELETE FROM messages WHERE session_id = ?",
                (session_id,)
            )

            # Delete session
            cursor.execute(
                "DELETE FROM sessions WHERE session_id = ?",
                (session_id,)
            )

            conn.commit()

    def _get_message_type(self, message: BaseMessage) -> str:
        """Get string type for LangChain message.

        Args:
            message: LangChain message object.

        Returns:
            String type: 'human', 'ai', or 'system'.
        """
        if isinstance(message, HumanMessage):
            return "human"
        elif isinstance(message, AIMessage):
            return "ai"
        elif isinstance(message, SystemMessage):
            return "system"
        else:
            return "unknown"

    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists in SQLite.

        Args:
            session_id: Unique session identifier.

        Returns:
            True if session exists, False otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM sessions WHERE session_id = ?",
                (session_id,)
            )
            return cursor.fetchone()[0] > 0

    def get_session_owner(self, session_id: str) -> int | None:
        """Get the user_id that owns a session.

        Args:
            session_id: Unique session identifier.

        Returns:
            The owner's user_id, or None if not set.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id FROM sessions WHERE session_id = ?",
                (session_id,)
            )
            row = cursor.fetchone()
            return row[0] if row and row[0] else None

    def bind_session_to_user(self, session_id: str, user_id: int) -> None:
        """Bind a session to a user.

        Creates the session if it doesn't exist, or updates the user_id.

        Args:
            session_id: Unique session identifier.
            user_id: The user's database ID.
        """
        now = datetime.utcnow().isoformat()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO sessions
                    (session_id, user_id, summary, created_at, last_accessed)
                VALUES (?, ?, ?, ?, ?)
                """,
                (session_id, user_id, None, now, now)
            )
            conn.commit()

    def save_embedding(self, session_id: str, position: int, embedding: list[float]) -> None:
        """Save embedding for a message.

        Args:
            session_id: Unique session identifier.
            position: Message position in session.
            embedding: Embedding vector as list of floats.
        """
        now = datetime.utcnow().isoformat()
        embedding_blob = json.dumps(embedding).encode()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO message_embeddings (session_id, position, embedding, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (session_id, position, embedding_blob, now)
            )
            conn.commit()

    def save_summary_embedding(self, session_id: str, embedding: list[float]) -> None:
        """Save embedding for a summary.

        Args:
            session_id: Unique session identifier.
            embedding: Embedding vector as list of floats.
        """
        now = datetime.utcnow().isoformat()
        embedding_blob = json.dumps(embedding).encode()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO summary_embeddings (session_id, embedding, created_at)
                VALUES (?, ?, ?)
                """,
                (session_id, embedding_blob, now)
            )
            conn.commit()

    def load_session_embeddings(self, session_id: str) -> list[tuple[int, BaseMessage, list[float] | None]]:
        """Load all messages with their embeddings for a session.

        Args:
            session_id: Unique session identifier.

        Returns:
            List of tuples (position, message, embedding) for each message.
            Messages without embeddings have None for the embedding value.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Load all messages for the session
            cursor.execute(
                "SELECT message_type, content, timestamp, order_in_session "
                "FROM messages WHERE session_id = ? ORDER BY order_in_session ASC",
                (session_id,)
            )
            message_rows = cursor.fetchall()

            # Load all embeddings for the session
            cursor.execute(
                "SELECT position, embedding FROM message_embeddings WHERE session_id = ?",
                (session_id,)
            )
            embedding_rows = cursor.fetchall()

            # Create a mapping of position to embedding
            embedding_map: dict[int, list[float]] = {}
            for position, embedding_blob in embedding_rows:
                try:
                    embedding = json.loads(embedding_blob.decode())
                    embedding_map[position] = embedding
                except (json.JSONDecodeError, AttributeError):
                    # Skip corrupted embeddings
                    continue

            # Combine messages with embeddings
            result: list[tuple[int, BaseMessage, list[float] | None]] = []
            for msg_type, content, timestamp, position in message_rows:
                # Reconstruct message object with timestamp in metadata
                if msg_type == "human":
                    message = HumanMessage(
                        content=content,
                        additional_kwargs={"timestamp": timestamp}
                    )
                elif msg_type == "ai":
                    message = AIMessage(
                        content=content,
                        additional_kwargs={"timestamp": timestamp}
                    )
                elif msg_type == "system":
                    message = SystemMessage(
                        content=content,
                        additional_kwargs={"timestamp": timestamp}
                    )
                else:
                    continue

                # Get embedding if it exists
                embedding = embedding_map.get(position)
                result.append((position, message, embedding))

            return result

    def save_execution_state(self, session_id: str, execution_state: dict[str, Any]) -> None:
        """Save execution state for a session.

        Args:
            session_id: Unique session identifier.
            execution_state: Execution state dictionary.
        """
        now = datetime.utcnow().isoformat()
        current_plan = json.dumps(execution_state.get("current_plan"))
        completed_steps = json.dumps(execution_state.get("completed_steps", []))
        pending_steps = json.dumps(execution_state.get("pending_steps", []))
        current_step = execution_state.get("current_step")
        execution_status = execution_state.get("execution_status", "idle")

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO execution_state (
                    session_id, current_plan, current_step, completed_steps,
                    pending_steps, execution_status, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    current_plan,
                    current_step,
                    completed_steps,
                    pending_steps,
                    execution_status,
                    now,
                )
            )
            conn.commit()

    def load_execution_state(self, session_id: str) -> dict[str, Any] | None:
        """Load execution state for a session.

        Args:
            session_id: Unique session identifier.

        Returns:
            Execution state dictionary, or None if not found.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT current_plan, current_step, completed_steps, pending_steps, execution_status "
                "FROM execution_state WHERE session_id = ?",
                (session_id,)
            )
            row = cursor.fetchone()

            if not row:
                return None

            current_plan, current_step, completed_steps, pending_steps, execution_status = row

            return {
                "current_plan": json.loads(current_plan) if current_plan else None,
                "current_step": current_step,
                "completed_steps": json.loads(completed_steps) if completed_steps else [],
                "pending_steps": json.loads(pending_steps) if pending_steps else [],
                "execution_status": execution_status,
            }

    def clear_execution_state(self, session_id: str) -> None:
        """Clear execution state for a session.

        Args:
            session_id: Unique session identifier.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM execution_state WHERE session_id = ?",
                (session_id,)
            )
            conn.commit()
