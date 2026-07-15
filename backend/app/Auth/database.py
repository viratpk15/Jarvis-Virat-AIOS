"""
Jarvis AIOS
-----------
Authentication Database

SQLite-backed user storage with parameterized queries.
All operations are isolated to the auth database.
"""

import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from app.Config.settings import AUTH_DB_PATH

logger = logging.getLogger(__name__)


class UserDatabase:
    """SQLite database for user authentication.

    Manages the users table with secure password storage.
    All SQL operations use parameterized queries.
    """

    def __init__(self, db_path: str = AUTH_DB_PATH):
        """Initialize the user database.

        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self._ensure_tables_exist()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection.

        Returns:
            SQLite connection object.
        """
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(self.db_path)

    def _ensure_tables_exist(self) -> None:
        """Create the users table if it doesn't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()
            logger.debug("Ensured users table exists at %s", self.db_path)

    def create_user(self, email: str, password_hash: str) -> int:
        """Create a new user.

        Args:
            email: The user's email address.
            password_hash: The bcrypt-hashed password.

        Returns:
            The new user's ID.

        Raises:
            ValueError: If the email is already registered.
        """
        now = datetime.now(timezone.utc).isoformat()

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
                    (email, password_hash, now),
                )
                conn.commit()
                user_id = cursor.lastrowid
                logger.info("Created user id=%s email=%s", user_id, email)
                return user_id
        except sqlite3.IntegrityError:
            raise ValueError(f"Email '{email}' is already registered")

    def get_user_by_email(self, email: str) -> dict | None:
        """Get a user by email.

        Args:
            email: The user's email address.

        Returns:
            User dict with id, email, password_hash, or None if not found.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, email, password_hash FROM users WHERE email = ?",
                (email,),
            )
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "email": row[1],
                    "password_hash": row[2],
                }
            return None

    def get_user_by_id(self, user_id: int) -> dict | None:
        """Get a user by ID.

        Args:
            user_id: The user's database ID.

        Returns:
            User dict with id and email, or None if not found.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, email FROM users WHERE id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "email": row[1],
                }
            return None


# Global database instance
user_db = UserDatabase()