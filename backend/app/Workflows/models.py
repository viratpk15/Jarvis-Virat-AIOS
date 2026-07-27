# backend/app/Workflows/models.py
"""
Jarvis AIOS — SQLAlchemy Data Models for Workflow Studio Subsystem (Sprint 6.7B).

Defines schemas for:
- WorkflowDefinitionModel: Graph topology (nodes, edges, variables) in JSON & YAML.
- WorkflowVersionModel: Immutable version history of workflow definitions.
- WorkflowExecutionModel: LangGraph execution instances, latency, token usage, and status.
- WorkflowNodeLogModel: Fine-grained per-node execution logs & input/output state snapshots.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
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


class WorkflowDefinitionModel(Base):
    """SQLAlchemy model for Workflow Graph Definitions."""

    __allow_unmapped__ = True
    __tablename__ = "workflow_definitions"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    workflow_id: str = Column(String(100), nullable=False, unique=True, index=True)
    name: str = Column(String(150), nullable=False)
    description: Optional[str] = Column(Text, nullable=True)
    is_active: bool = Column(Boolean, nullable=False, default=True)
    definition_json: str = Column(Text, nullable=False, default="{}")
    definition_yaml: Optional[str] = Column(Text, nullable=True)
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: datetime = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    versions = relationship("WorkflowVersionModel", back_populates="workflow", cascade="all, delete-orphan")
    executions = relationship("WorkflowExecutionModel", back_populates="workflow", cascade="all, delete-orphan")


class WorkflowVersionModel(Base):
    """SQLAlchemy model for Workflow Version Control."""

    __allow_unmapped__ = True
    __tablename__ = "workflow_versions"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    workflow_id: int = Column(
        Integer, ForeignKey("workflow_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_number: int = Column(Integer, nullable=False, default=1)
    definition_json: str = Column(Text, nullable=False)
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    workflow = relationship("WorkflowDefinitionModel", back_populates="versions")


class WorkflowExecutionModel(Base):
    """SQLAlchemy model for LangGraph Workflow Execution Runs."""

    __allow_unmapped__ = True
    __tablename__ = "workflow_executions"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    execution_id: str = Column(String(100), nullable=False, unique=True, index=True)
    workflow_id: int = Column(
        Integer, ForeignKey("workflow_definitions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: str = Column(String(50), nullable=False, default="running", index=True)  # running, paused, completed, failed, cancelled
    total_latency_ms: float = Column(Float, nullable=False, default=0.0)
    total_tokens: int = Column(Integer, nullable=False, default=0)
    total_cost: float = Column(Float, nullable=False, default=0.0)
    started_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    completed_at: Optional[datetime] = Column(DateTime(timezone=True), nullable=True)

    workflow = relationship("WorkflowDefinitionModel", back_populates="executions")
    logs = relationship("WorkflowNodeLogModel", back_populates="execution", cascade="all, delete-orphan")


class WorkflowNodeLogModel(Base):
    """SQLAlchemy model for individual node execution logs & state checkpoints."""

    __allow_unmapped__ = True
    __tablename__ = "workflow_node_logs"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    execution_id: int = Column(
        Integer, ForeignKey("workflow_executions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    node_id: str = Column(String(100), nullable=False, index=True)
    node_type: str = Column(String(50), nullable=False)
    status: str = Column(String(50), nullable=False, default="success")
    latency_ms: float = Column(Float, nullable=False, default=0.0)
    input_json: str = Column(Text, nullable=False, default="{}")
    output_json: str = Column(Text, nullable=False, default="{}")
    timestamp: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    execution = relationship("WorkflowExecutionModel", back_populates="logs")

    __table_args__ = (
        Index("idx_node_log_exec_time", "execution_id", "timestamp"),
    )
