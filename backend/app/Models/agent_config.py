"""
Jarvis AIOS
-----------
Agent Configuration Model

Pydantic model for agent configuration. Used to define agent identity
and enabled state. Future implementations may extend this with additional
configuration fields like capabilities, routes, or custom parameters.
"""

from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Configuration for an agent.

    Defines the identity and enabled state of an agent.
    Used by AgentRegistry to manage agent lifecycle.

    Attributes:
        name: Unique identifier for the agent.
        description: Human-readable description of the agent's purpose.
        enabled: Whether the agent is currently active.
    """

    name: str = Field(..., min_length=1, description="Unique agent identifier.")
    description: str = Field(
        default="", description="Human-readable description of agent capabilities."
    )
    enabled: bool = Field(default=True, description="Whether the agent is active.")