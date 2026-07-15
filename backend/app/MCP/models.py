"""
Jarvis AIOS
-----------
MCP Configuration Models

Pydantic models for MCP server configuration validation.
Provides structured configuration that can be loaded from environment
variables or configuration files.
"""

from typing import Optional

from pydantic import BaseModel, Field


class MCPServerConfigModel(BaseModel):
    """Pydantic model for MCP server configuration.

    Used to validate MCP server configuration at runtime.
    Future implementations can load this from JSON/YAML config files.

    Attributes:
        name: Unique identifier for the MCP server.
        description: Human-readable description of the server.
        enabled: Whether the server is active.
        command: Optional command to launch the server (for subprocess MCP servers).
        args: Optional arguments for the server command.
        env: Optional environment variables for the server.
        timeout: Timeout in seconds for tool execution (default 30).
    """

    name: str = Field(..., min_length=1, description="Unique server identifier")
    description: str = Field(default="", description="Server description")
    enabled: bool = Field(default=True, description="Whether server is enabled")
    command: Optional[str] = Field(default=None, description="Launch command")
    args: list[str] = Field(default_factory=list, description="Launch arguments")
    env: dict[str, str] = Field(default_factory=dict, description="Environment variables")
    timeout: int = Field(default=30, ge=1, le=300, description="Execution timeout in seconds")

    class Config:
        """Pydantic model configuration."""
        frozen = True  # Immutable after creation


class MCPConfigModel(BaseModel):
    """Root configuration model for MCP integration.

    Attributes:
        servers: List of MCP server configurations.
        auto_register: Whether to auto-register enabled servers on startup.
    """

    servers: list[MCPServerConfigModel] = Field(
        default_factory=list,
        description="List of MCP server configurations"
    )
    auto_register: bool = Field(
        default=False,
        description="Auto-register servers on startup"
    )

    class Config:
        """Pydantic model configuration."""
        frozen = True

    def get_enabled_servers(self) -> list[MCPServerConfigModel]:
        """Get list of enabled server configurations.

        Returns:
            List of servers where enabled=True.
        """
        return [s for s in self.servers if s.enabled]