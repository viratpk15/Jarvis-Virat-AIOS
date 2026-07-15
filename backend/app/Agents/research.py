"""
Jarvis AIOS
-----------
Research Agent

Concrete agent implementation for research-oriented requests.
Uses Browser MCP to perform web searches and information gathering.
"""

from typing import Any

from app.Agents.agent import Agent
from app.Models.agent_config import AgentConfig
from app.MCP import get_browser_server


# Global ResearchAgent instance
_research_agent: "ResearchAgent | None" = None


class ResearchAgent(Agent):
    """Agent for research and web-based information gathering.

    Handles requests involving search, lookup, or research operations.
    Uses Browser MCP to perform web searches with mock responses.
    """

    config = AgentConfig(
        name="research_agent",
        description="Handles web search and information gathering requests",
        enabled=True,
    )

    def can_handle(self, request: Any) -> bool:
        """Check if this agent can handle the given request.

        Args:
            request: The request to evaluate.

        Returns:
            True if the request contains research-oriented keywords.
        """
        keywords = ["search", "find", "look up", "research", "lookup"]
        request_str = str(request).lower()
        return any(kw in request_str for kw in keywords)

    def execute(self, request: Any) -> Any:
        """Execute the research agent's logic.

        Uses Browser MCP to search the web for the given query.

        Args:
            request: The search query string.

        Returns:
            The Browser MCP search results unchanged.
        """
        client = get_browser_server()
        client.initialize()
        return client.execute_tool("search_web", query=str(request))


def get_research_agent() -> ResearchAgent:
    """Get or create the global ResearchAgent instance.

    Returns:
        The ResearchAgent singleton.
    """
    global _research_agent
    if _research_agent is None:
        _research_agent = ResearchAgent()
    return _research_agent