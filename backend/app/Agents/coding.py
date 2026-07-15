"""
Jarvis AIOS
-----------
Coding Agent

Concrete agent implementation for coding-related requests.
Uses GitHub and Filesystem MCP to read code and repository information.
"""

from typing import Any

from app.Agents.agent import Agent
from app.Models.agent_config import AgentConfig
from app.MCP import get_github_server, get_filesystem_server


# Global CodingAgent instance
_coding_agent: "CodingAgent | None" = None


class CodingAgent(Agent):
    """Agent for coding and repository-related requests.

    Handles requests involving code, bugs, repositories, etc.
    Uses GitHub MCP and Filesystem MCP for read-only operations.
    """

    config = AgentConfig(
        name="coding_agent",
        description="Handles code and repository operations",
        enabled=True,
    )

    def can_handle(self, request: Any) -> bool:
        """Check if this agent can handle the given request.

        Args:
            request: The request to evaluate.

        Returns:
            True if the request contains coding-oriented keywords.
        """
        keywords = ["code", "function", "class", "bug", "error", "fix", "repository", "github"]
        request_str = str(request).lower()
        return any(kw in request_str for kw in keywords)

    def execute(self, request: Any) -> dict[str, Any]:
        """Execute the coding agent's logic.

        Uses GitHub MCP to get repository info and Filesystem MCP to read files.

        Args:
            request: The coding request string.

        Returns:
            The MCP server response with mock repository data.
        """
        client = get_github_server()
        client.initialize()
        return client.execute_tool("get_repository", owner="testuser", repo="testrepo")


def get_coding_agent() -> CodingAgent:
    """Get or create the global CodingAgent instance.

    Returns:
        The CodingAgent singleton.
    """
    global _coding_agent
    if _coding_agent is None:
        _coding_agent = CodingAgent()
    return _coding_agent