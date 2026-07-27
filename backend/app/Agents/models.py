# backend/app/Agents/models.py
"""SQLAlchemy ORM models for Agent Studio.

Uses the existing SQLAlchemy Base from `app.Data.base` — consistent with every
other model in the project. No SQLModel dependency required.

Tables created by Alembic migration: a1b2c3d4e5f6_initial_agent_studio_schema
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.Data.base import Base


class Agent(Base):
    """An agent definition — the top-level entity in Agent Studio."""

    __allow_unmapped__ = True
    __tablename__ = "agent"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False, index=True)
    description: Optional[str] = Column(Text, nullable=True)
    is_active: bool = Column(Boolean, nullable=False, default=True)
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: datetime = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    versions: List["AgentVersion"] = relationship(
        "AgentVersion", back_populates="agent", cascade="all, delete-orphan"
    )
    teams: List["AgentTeam"] = relationship(
        "AgentTeam", back_populates="agent", cascade="all, delete-orphan"
    )


class AgentVersion(Base):
    """A pinned snapshot of an agent's configuration."""

    __allow_unmapped__ = True
    __tablename__ = "agentversion"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    agent_id: int = Column(Integer, ForeignKey("agent.id", ondelete="CASCADE"), nullable=False)
    version_number: int = Column(Integer, nullable=False)
    changelog: Optional[str] = Column(Text, nullable=True)
    is_current: bool = Column(Boolean, nullable=False, default=False)
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relationships
    agent: "Agent" = relationship("Agent", back_populates="versions")
    prompt_bindings: List["AgentPromptBinding"] = relationship(
        "AgentPromptBinding", back_populates="version", cascade="all, delete-orphan"
    )
    tool_bindings: List["AgentToolBinding"] = relationship(
        "AgentToolBinding", back_populates="version", cascade="all, delete-orphan"
    )
    memory_bindings: List["AgentMemoryBinding"] = relationship(
        "AgentMemoryBinding", back_populates="version", cascade="all, delete-orphan"
    )
    model_bindings: List["AgentModelBinding"] = relationship(
        "AgentModelBinding", back_populates="version", cascade="all, delete-orphan"
    )
    executions: List["AgentExecution"] = relationship(
        "AgentExecution", back_populates="version", cascade="all, delete-orphan"
    )


class AgentPromptBinding(Base):
    """Links a version to a Prompt Studio prompt."""

    __allow_unmapped__ = True
    __tablename__ = "agentpromptbinding"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    version_id: int = Column(
        Integer, ForeignKey("agentversion.id", ondelete="CASCADE"), nullable=False
    )
    prompt_id: int = Column(Integer, nullable=False)  # FK to prompt table (Prompt Studio)

    version: "AgentVersion" = relationship("AgentVersion", back_populates="prompt_bindings")


class AgentToolBinding(Base):
    """Links a version to a registered Tool Engine tool."""

    __allow_unmapped__ = True
    __tablename__ = "agenttoolbinding"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    version_id: int = Column(
        Integer, ForeignKey("agentversion.id", ondelete="CASCADE"), nullable=False
    )
    tool_name: str = Column(String, nullable=False)
    config_json: Optional[str] = Column(Text, nullable=True)

    version: "AgentVersion" = relationship("AgentVersion", back_populates="tool_bindings")


class AgentMemoryBinding(Base):
    """Links a version to a MemoryManager key."""

    __allow_unmapped__ = True
    __tablename__ = "agentmemorybinding"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    version_id: int = Column(
        Integer, ForeignKey("agentversion.id", ondelete="CASCADE"), nullable=False
    )
    memory_key: str = Column(String, nullable=False)
    config_json: Optional[str] = Column(Text, nullable=True)

    version: "AgentVersion" = relationship("AgentVersion", back_populates="memory_bindings")


class AgentModelBinding(Base):
    """Links a version to a model configuration (temperature, model name, etc.)."""

    __allow_unmapped__ = True
    __tablename__ = "agentmodelbinding"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    version_id: int = Column(
        Integer, ForeignKey("agentversion.id", ondelete="CASCADE"), nullable=False
    )
    model_name: str = Column(String, nullable=False)
    parameters_json: Optional[str] = Column(Text, nullable=True)

    version: "AgentVersion" = relationship("AgentVersion", back_populates="model_bindings")


class AgentExecution(Base):
    """A single run of an agent version through the LangGraph runtime."""

    __allow_unmapped__ = True
    __tablename__ = "agentexecution"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    version_id: int = Column(
        Integer, ForeignKey("agentversion.id", ondelete="CASCADE"), nullable=False
    )
    run_id: Optional[str] = Column(String, nullable=True)
    status: str = Column(String, nullable=False, default="draft")
    started_at: Optional[datetime] = Column(DateTime, nullable=True)
    finished_at: Optional[datetime] = Column(DateTime, nullable=True)
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relationships
    version: "AgentVersion" = relationship("AgentVersion", back_populates="executions")
    steps: List["ExecutionStep"] = relationship(
        "ExecutionStep", back_populates="execution", cascade="all, delete-orphan"
    )


class ExecutionStep(Base):
    """One step within an agent execution."""

    __allow_unmapped__ = True
    __tablename__ = "executionstep"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    execution_id: int = Column(
        Integer, ForeignKey("agentexecution.id", ondelete="CASCADE"), nullable=False
    )
    step_index: int = Column(Integer, nullable=False)
    name: str = Column(String, nullable=False)
    status: str = Column(String, nullable=False, default="pending")
    input_data: Optional[str] = Column(Text, nullable=True)
    output_data: Optional[str] = Column(Text, nullable=True)

    execution: "AgentExecution" = relationship("AgentExecution", back_populates="steps")


class AgentTeam(Base):
    """A named multi-agent team graph owned by a parent agent."""

    __allow_unmapped__ = True
    __tablename__ = "agentteam"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    agent_id: int = Column(Integer, ForeignKey("agent.id", ondelete="CASCADE"), nullable=False)
    name: str = Column(String, nullable=False)

    agent: "Agent" = relationship("Agent", back_populates="teams")
    nodes: List["TeamAgentNode"] = relationship(
        "TeamAgentNode", back_populates="team", cascade="all, delete-orphan"
    )
    edges: List["TeamEdge"] = relationship(
        "TeamEdge", back_populates="team", cascade="all, delete-orphan"
    )


class TeamAgentNode(Base):
    """A node in a team graph — references an agent version with a canvas position."""

    __allow_unmapped__ = True
    __tablename__ = "teamagentnode"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    team_id: int = Column(Integer, ForeignKey("agentteam.id", ondelete="CASCADE"), nullable=False)
    agent_version_id: int = Column(
        Integer, ForeignKey("agentversion.id", ondelete="CASCADE"), nullable=False
    )
    position_x: float = Column(Float, nullable=False, default=0.0)
    position_y: float = Column(Float, nullable=False, default=0.0)

    team: "AgentTeam" = relationship("AgentTeam", back_populates="nodes")
    version: "AgentVersion" = relationship("AgentVersion")


class TeamEdge(Base):
    """A directed edge in a team graph with optional conditional routing."""

    __allow_unmapped__ = True
    __tablename__ = "teamedge"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    team_id: int = Column(Integer, ForeignKey("agentteam.id", ondelete="CASCADE"), nullable=False)
    source_node_id: int = Column(
        Integer, ForeignKey("teamagentnode.id", ondelete="CASCADE"), nullable=False
    )
    target_node_id: int = Column(
        Integer, ForeignKey("teamagentnode.id", ondelete="CASCADE"), nullable=False
    )
    condition_json: Optional[str] = Column(Text, nullable=True)

    team: "AgentTeam" = relationship("AgentTeam", back_populates="edges")
