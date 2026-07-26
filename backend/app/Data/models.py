"""
Jarvis AIOS
-----------
SQLAlchemy Data Models

Defines infrastructure ORM schemas for users, sessions, messages, memory embeddings,
and execution state for PostgreSQL (Supabase) and database migration support.
"""

from sqlalchemy import (
    Column,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.Data.base import Base


class UserModel(Base):
    """SQLAlchemy model for user authentication storage."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(String(100), nullable=False)

    # Relationships
    sessions = relationship("SessionModel", back_populates="user", cascade="all, delete-orphan")


class SessionModel(Base):
    """SQLAlchemy model for chat sessions and conversation threads."""

    __tablename__ = "sessions"

    session_id = Column(String(255), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(255), default="New Conversation", nullable=False)
    pinned = Column(Integer, default=0, nullable=False)
    summary = Column(Text, nullable=True)
    created_at = Column(String(100), nullable=False)
    last_accessed = Column(String(100), nullable=False)

    # Relationships
    user = relationship("UserModel", back_populates="sessions")
    messages = relationship("MessageModel", back_populates="session", cascade="all, delete-orphan")
    message_embeddings = relationship("MessageEmbeddingModel", back_populates="session", cascade="all, delete-orphan")
    summary_embedding = relationship("SummaryEmbeddingModel", back_populates="session", uselist=False, cascade="all, delete-orphan")
    execution_state = relationship("ExecutionStateModel", back_populates="session", uselist=False, cascade="all, delete-orphan")


class MessageModel(Base):
    """SQLAlchemy model for conversation chat messages."""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), ForeignKey("sessions.session_id", ondelete="CASCADE"), nullable=False)
    message_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(String(100), nullable=False)
    order_in_session = Column(Integer, nullable=False)

    # Relationships
    session = relationship("SessionModel", back_populates="messages")

    __table_args__ = (
        Index("idx_messages_session_order", "session_id", "order_in_session"),
    )


class MessageEmbeddingModel(Base):
    """SQLAlchemy model for message vector embeddings."""

    __tablename__ = "message_embeddings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), ForeignKey("sessions.session_id", ondelete="CASCADE"), nullable=False)
    position = Column(Integer, nullable=False)
    embedding = Column(LargeBinary, nullable=False)
    created_at = Column(String(100), nullable=False)

    # Relationships
    session = relationship("SessionModel", back_populates="message_embeddings")

    __table_args__ = (
        Index("idx_embeddings_session_pos", "session_id", "position"),
    )


class SummaryEmbeddingModel(Base):
    """SQLAlchemy model for conversation summary vector embeddings."""

    __tablename__ = "summary_embeddings"

    session_id = Column(String(255), ForeignKey("sessions.session_id", ondelete="CASCADE"), primary_key=True)
    embedding = Column(LargeBinary, nullable=False)
    created_at = Column(String(100), nullable=False)

    # Relationships
    session = relationship("SessionModel", back_populates="summary_embedding")


class ExecutionStateModel(Base):
    """SQLAlchemy model for plan execution state persistence."""

    __tablename__ = "execution_state"

    session_id = Column(String(255), ForeignKey("sessions.session_id", ondelete="CASCADE"), primary_key=True)
    current_plan = Column(Text, nullable=True)
    current_step = Column(Integer, nullable=True)
    completed_steps = Column(Text, nullable=False, default="[]")
    pending_steps = Column(Text, nullable=False, default="[]")
    execution_status = Column(String(50), nullable=False, default="idle")
    updated_at = Column(String(100), nullable=False)

    # Relationships
    session = relationship("SessionModel", back_populates="execution_state")
