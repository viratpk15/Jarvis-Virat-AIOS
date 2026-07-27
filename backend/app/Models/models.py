# backend/app/Models/models.py
"""
Jarvis AIOS — SQLAlchemy Data Models for Model Studio Subsystem.

Defines schemas for:
- ProviderConfigModel: 15+ LLM Provider configurations & encrypted credentials.
- LLMModelConfigModel: Registered language model parameters, context limits & cost rates.
- RoutingPolicyModel: Model routing rules, fallback chains & load balancing.
- BenchmarkRunModel: Latency benchmarks, TTFT, and throughput metrics.
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


class ProviderConfigModel(Base):
    """SQLAlchemy model for LLM Providers & encrypted API key credentials."""

    __allow_unmapped__ = True
    __tablename__ = "provider_configs"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    provider_name: str = Column(String(50), nullable=False, unique=True, index=True)
    display_name: str = Column(String(100), nullable=False)
    api_base_url: str = Column(String(255), nullable=False)
    encrypted_api_key: Optional[str] = Column(Text, nullable=True)
    is_enabled: bool = Column(Boolean, nullable=False, default=True)
    is_healthy: bool = Column(Boolean, nullable=False, default=True)
    latency_ms: float = Column(Float, nullable=False, default=0.0)
    updated_at: datetime = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Relationship to models
    models = relationship(
        "LLMModelConfigModel", back_populates="provider", cascade="all, delete-orphan"
    )


class LLMModelConfigModel(Base):
    """SQLAlchemy model for specific LLM configuration parameters."""

    __allow_unmapped__ = True
    __tablename__ = "llm_model_configs"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    provider_id: int = Column(
        Integer, ForeignKey("provider_configs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    model_id: str = Column(String(100), nullable=False, unique=True, index=True)
    display_name: str = Column(String(100), nullable=False)
    context_window: int = Column(Integer, nullable=False, default=128000)
    max_output_tokens: int = Column(Integer, nullable=False, default=4096)
    input_cost_per_1k: float = Column(Float, nullable=False, default=0.0015)
    output_cost_per_1k: float = Column(Float, nullable=False, default=0.0020)
    is_active: bool = Column(Boolean, nullable=False, default=True)
    is_default: bool = Column(Boolean, nullable=False, default=False)
    routing_priority: int = Column(Integer, nullable=False, default=10)
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relationship back to provider
    provider = relationship("ProviderConfigModel", back_populates="models")


class RoutingPolicyModel(Base):
    """SQLAlchemy model for Model Studio fallback chains & routing policies."""

    __allow_unmapped__ = True
    __tablename__ = "routing_policies"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    policy_name: str = Column(String(100), nullable=False, unique=True, index=True)
    description: Optional[str] = Column(Text, nullable=True)
    is_active: bool = Column(Boolean, nullable=False, default=True)
    config_json: str = Column(Text, nullable=False, default="{}")
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class BenchmarkRunModel(Base):
    """SQLAlchemy model for LLM latency & benchmark historical runs."""

    __allow_unmapped__ = True
    __tablename__ = "benchmark_runs"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    model_id: str = Column(String(100), nullable=False, index=True)
    prompt_tokens: int = Column(Integer, nullable=False, default=0)
    completion_tokens: int = Column(Integer, nullable=False, default=0)
    total_latency_ms: float = Column(Float, nullable=False, default=0.0)
    ttft_ms: float = Column(Float, nullable=False, default=0.0)
    status: str = Column(String(50), nullable=False, default="success")
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        Index("idx_benchmark_model_date", "model_id", "created_at"),
    )
