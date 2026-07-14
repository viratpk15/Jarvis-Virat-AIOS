"""
Memory Persistence Layer

Provides SQLite-backed persistent storage for conversation history and summaries.
All persistence operations are encapsulated in this layer to ensure clean separation
of concerns and prevent SQL injection through parameterized queries.
"""

from app.Memory.persistence.sqlite_backend import SQLitePersistenceBackend

__all__ = ["SQLitePersistenceBackend"]