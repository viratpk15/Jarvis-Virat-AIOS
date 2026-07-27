# backend/app/Memory/models.py
"""
Jarvis AIOS — SQLAlchemy Data Models for Memory Studio Subsystem.

Defines schemas for:
- EpisodicEventModel: Task execution milestones, retry logs, and tool execution snapshots.
- MemoryEntityModel: Named entities for the Semantic Knowledge Graph.
- MemoryRelationModel: Directed triples (Subject -> Predicate -> Object) for Semantic Graph.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.Data.base import Base


class EpisodicEventModel(Base):
    """SQLAlchemy model for Episodic Memory event logs and execution snapshots."""

    __allow_unmapped__ = True
    __tablename__ = "episodic_events"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    session_id: str = Column(
        String(255), ForeignKey("sessions.session_id", ondelete="CASCADE"), nullable=False, index=True
    )
    run_id: Optional[str] = Column(String(255), nullable=True)
    step_index: int = Column(Integer, nullable=False, default=0)
    event_type: str = Column(String(50), nullable=False, index=True)
    payload_json: str = Column(Text, nullable=False, default="{}")
    outcome: str = Column(String(50), nullable=False, default="success")
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relationship
    session = relationship("SessionModel", backref="episodic_events")

    __table_args__ = (
        Index("idx_episodic_session_step", "session_id", "step_index"),
    )


class MemoryEntityModel(Base):
    """SQLAlchemy model for Semantic Memory entity nodes."""

    __allow_unmapped__ = True
    __tablename__ = "memory_entities"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: Optional[int] = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True
    )
    entity_name: str = Column(String(255), nullable=False, index=True)
    entity_category: str = Column(String(100), nullable=False, default="Concept", index=True)
    attributes_json: Optional[str] = Column(Text, nullable=True, default="{}")
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relationships
    subject_relations = relationship(
        "MemoryRelationModel",
        foreign_keys="[MemoryRelationModel.subject_entity_id]",
        back_populates="subject_entity",
        cascade="all, delete-orphan",
    )
    object_relations = relationship(
        "MemoryRelationModel",
        foreign_keys="[MemoryRelationModel.object_entity_id]",
        back_populates="object_entity",
        cascade="all, delete-orphan",
    )


class MemoryRelationModel(Base):
    """SQLAlchemy model for Semantic Memory entity-relation triples."""

    __allow_unmapped__ = True
    __tablename__ = "memory_relations"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    subject_entity_id: int = Column(
        Integer, ForeignKey("memory_entities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    object_entity_id: int = Column(
        Integer, ForeignKey("memory_entities.id", ondelete="CASCADE"), nullable=False, index=True
    )
    relation_type: str = Column(String(100), nullable=False, index=True)
    confidence: float = Column(Float, nullable=False, default=1.0)
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relationships
    subject_entity = relationship(
        "MemoryEntityModel", foreign_keys=[subject_entity_id], back_populates="subject_relations"
    )
    object_entity = relationship(
        "MemoryEntityModel", foreign_keys=[object_entity_id], back_populates="object_relations"
    )
