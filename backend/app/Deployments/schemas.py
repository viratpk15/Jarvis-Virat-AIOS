# backend/app/Deployments/schemas.py
"""
Jarvis AIOS — Pydantic Schemas for Deployment Studio REST API.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DeploymentEnvironmentResponse(BaseModel):
    id: int
    env_id: str
    name: str
    tier: str
    is_active: bool
    created_at: datetime


class EnvironmentCreatePayload(BaseModel):
    env_id: str = Field(..., example="staging")
    name: str = Field(..., example="Staging Pre-Release Environment")
    tier: str = Field("staging", example="staging")


class DeploymentTargetResponse(BaseModel):
    id: int
    env_id: int
    provider_type: str
    config: Dict[str, Any]
    status: str
    created_at: datetime


class TargetRegisterPayload(BaseModel):
    env_id: str = Field(..., example="prod")
    provider_type: str = Field(..., example="kubernetes")
    config: Dict[str, Any] = Field(default_factory=dict)


class RolloutTriggerPayload(BaseModel):
    env_id: str = Field("prod", example="prod")
    version_tag: str = Field(..., example="v1.8.0")
    strategy: str = Field("blue_green", example="blue_green")


class RolloutResponse(BaseModel):
    release_id: str
    environment: str
    version_tag: str
    strategy: str
    status: str
    rollout_duration_s: float
    deployed_at: datetime


class RollbackTriggerPayload(BaseModel):
    env_id: str = Field("prod", example="prod")
    target_release_id: Optional[str] = Field(None, example="rel_v1_7_0")


class SecretVaultEntryResponse(BaseModel):
    id: int
    secret_key: str
    masked_value: str
    updated_at: datetime


class SecretSavePayload(BaseModel):
    env_id: str = Field("prod", example="prod")
    secret_key: str = Field(..., example="OPENAI_API_KEY")
    raw_value: str = Field(..., example="sk-proj-super-secret-key-12345")


class DatabaseBackupResponse(BaseModel):
    id: int
    snapshot_name: str
    storage_path: str
    size_bytes: int
    created_at: datetime


class BackupRestorePayload(BaseModel):
    snapshot_name: str = Field(..., example="backup_prod_20260727_173000")


class ContainerProbe(BaseModel):
    name: str
    status: str
    latency_ms: float


class HealthMetricsResponse(BaseModel):
    environment: str
    status: str
    cpu_percent: float
    memory_mb: float
    containers_running: int
    probes: List[ContainerProbe]


class DeploymentAuditLogResponse(BaseModel):
    id: int
    action: str
    operator_user: str
    details: Dict[str, Any]
    timestamp: datetime
