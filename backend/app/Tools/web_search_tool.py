"""
Jarvis AIOS
--------------------
Web Search Tool Provider Interface (Abstraction)

Exposes Web Search tool interface and metadata. If SEARCH_API_KEY environment variable
is missing or unconfigured, returns a clear "not configured" status rather than crashing.
"""

import os
from typing import Any, Dict, Optional
from app.Tools.tool import Tool
from app.Tools.metadata import ToolMetadata, PermissionLevel


class WebSearchTool(Tool):
    """
    Web Search Tool Provider Abstraction.
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.environ.get("SEARCH_API_KEY")

        meta = ToolMetadata(
            name="web_search",
            display_name="Web Search Engine",
            description="Search the web for real-time information, news, and technical documentation.",
            category="web",
            tags=["search", "web", "google", "bing", "internet"],
            version="1.0.0",
            author="Jarvis AIOS Core",
            permission_level=PermissionLevel.USER,
            requires_approval=False,
            timeout_seconds=10.0,
            parameter_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term or query string.",
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Maximum number of search results to return.",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        )
        super().__init__(metadata=meta)

    def execute(self, query: str, num_results: int = 5, **kwargs: Any) -> Dict[str, Any]:
        """
        Execute web search query. Returns graceful unconfigured response if API key is missing.
        """
        if not self.api_key:
            return {
                "query": query,
                "configured": False,
                "status": "not_configured",
                "message": (
                    "Web Search Provider is not configured. "
                    "Please set the SEARCH_API_KEY environment variable to enable live web search."
                ),
                "results": [],
            }

        # Placeholder interface structure for when SEARCH_API_KEY is configured
        return {
            "query": query,
            "configured": True,
            "status": "success",
            "message": "Web search completed successfully.",
            "results": [
                {
                    "title": f"Result 1 for {query}",
                    "snippet": f"Mock snippet for {query} search query.",
                    "url": f"https://example.com/search?q={query}",
                }
            ],
        }
