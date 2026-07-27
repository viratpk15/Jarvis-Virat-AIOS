# backend/app/Deployments/models.py
"""
Jarvis AIOS — SQLAlchemy Data Models for Deployment Studio Subsystem (Sprint 6.8B).

Defines schemas for:
- DeploymentEnvironmentModel: Deployment stages (dev, staging, production).
- DeploymentTargetModel: Infrastructure providers (Docker, K8s, Railway, Render, Fly, AWS, GCP, Azure, Self-hosted).
- DeploymentReleaseModel: Deployment releases (Blue/Green, Canary, Direct) and health state.
- SecretVaultEntryModel: XOR/AES Encrypted environment variables and secrets at rest.
- DatabaseBackupModel: Database backup snapshot metadata and restore tracking.
- DeploymentAuditLogModel: Audit trail of deployment, rollback, and vault actions.
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


class DeploymentEnvironmentModel(Base):
    """SQLAlchemy model for Deployment Environments."""

    __allow_unmapped__ = True
    __tablename__ = "deployment_environments"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    env_id: str = Column(String(50), nullable=False, unique=True, index=True)
    name: str = Column(String(100), nullable=False)
    tier: str = Column(String(50), nullable=False, default="production")  # dev, staging, production
    is_active: bool = Column(Boolean, nullable=False, default=True)
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    targets = relationship("DeploymentTargetModel", back_populates="environment", cascade="all, delete-orphan")
    releases = relationship("DeploymentReleaseModel", back_populates="environment", cascade="all, delete-orphan")
    secrets = relationship("SecretVaultEntryModel", back_populates="environment", cascade="all, delete-orphan")
    backups = relationship("DatabaseBackupModel", back_populates="environment", cascade="all, delete-orphan")


class DeploymentTargetModel(Base):
    """SQLAlchemy model for Deployment Infrastructure Target Providers."""

    __allow_unmapped__ = True
    __tablename__ = "deployment_targets"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    env_id: int = Column(
        Integer, ForeignKey("deployment_environments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    provider_type: str = Column(String(50), nullable=False, index=True)  # docker, k8s, railway, render, vercel, fly, aws, gcp, azure, self_hosted
    config_json: str = Column(Text, nullable=False, default="{}")
    status: str = Column(String(50), nullable=False, default="active")
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    environment = relationship("DeploymentEnvironmentModel", back_populates="targets")


class DeploymentReleaseModel(Base):
    """SQLAlchemy model for Deployment Release Rollouts."""

    __allow_unmapped__ = True
    __tablename__ = "deployment_releases"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    release_id: str = Column(String(100), nullable=False, unique=True, index=True)
    env_id: int = Column(
        Integer, ForeignKey("deployment_environments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    version_tag: str = Column(String(50), nullable=False)
    strategy: str = Column(String(50), nullable=False, default="blue_green")  # blue_green, canary, direct
    status: str = Column(String(50), nullable=False, default="running", index=True)  # running, healthy, rolled_back, failed
    rollout_duration_s: float = Column(Float, nullable=False, default=0.0)
    deployed_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    environment = relationship("DeploymentEnvironmentModel", back_populates="releases")
    audit_logs = relationship("DeploymentAuditLogModel", back_populates="release", cascade="all, delete-orphan")


class SecretVaultEntryModel(Base):
    """SQLAlchemy model for Encrypted Secrets at rest."""

    __allow_unmapped__ = True
    __tablename__ = "secret_vault_entries"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    env_id: int = Column(
        Integer, ForeignKey("deployment_environments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    secret_key: str = Column(String(100), nullable=False)
    encrypted_value: str = Column(Text, nullable=False)
    updated_at: datetime = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    environment = relationship("DeploymentEnvironmentModel", back_populates="secrets")

    __table_args__ = (
        Index("idx_secret_env_key", "env_id", "secret_key", unique=True),
    )


class DatabaseBackupModel(Base):
    """SQLAlchemy model for Database Backup Snapshots."""

    __allow_unmapped__ = True
    __tablename__ = "database_backups"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    env_id: int = Column(
        Integer, ForeignKey("deployment_environments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    snapshot_name: str = Column(String(150), nullable=False, unique=True, index=True)
    storage_path: str = Column(String(255), nullable=False)
    size_bytes: int = Column(Integer, nullable=False, default=0)
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    environment = relationship("DeploymentEnvironmentModel", back_populates="backups")


class DeploymentAuditLogModel(Base):
    """SQLAlchemy model for Deployment Audit Trail Logs."""

    __allow_unmapped__ = True
    __tablename__ = "deployment_audit_logs"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    release_id: Optional[int] = Column(
        Integer, ForeignKey("deployment_releases.id", ondelete="SET NULL"), nullable=True, index=True
    )
    action: str = Column(String(100), nullable=False)  # rollout, rollback, secret_updated, backup_created
    operator_user: str = Column(String(100), nullable=False, default="admin")
    details_json: str = Column(Text, nullable=False, default="{}")
    timestamp: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    release = relationship("DeploymentReleaseModel", back_populates="audit_logs")
