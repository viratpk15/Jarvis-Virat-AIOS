"""
Jarvis AIOS
-----------
GitHub MCP Server

Read-only GitHub repository access through the Model Context Protocol.
Provides get_repository and list_repository_files tools with mocked
responses for provider-agnostic implementation.
"""

from typing import Any

from app.MCP.client import MCPClient, MCPServerConfig


class GitHubMCPClient(MCPClient):
    """GitHub MCP server with read-only repository access.

    Provides get_repository and list_repository_files tools for
    GitHub repository information. Uses mocked responses for now
    - can be replaced with real GitHub API calls later.
    """

    def __init__(self, config: MCPServerConfig | None = None) -> None:
        """Initialize the GitHub MCP client.

        Args:
            config: Optional MCP server configuration. If not provided,
                a default configuration is used.
        """
        self._config = config or MCPServerConfig(
            name="github",
            description="Read-only GitHub repository access via MCP.",
            enabled=True,
            capabilities=["get_repository", "list_repository_files"]
        )
        self._tools: dict[str, Any] = {}

    @property
    def config(self) -> MCPServerConfig:
        """Get the server configuration.

        Returns:
            The MCPServerConfig for this client.
        """
        return self._config

    def list_tools(self) -> list[str]:
        """List available tool names from this MCP server.

        Returns:
            List of tool names available on this server.
        """
        return list(self._tools.keys())

    def execute_tool(self, tool_name: str, **kwargs: Any) -> Any:
        """Execute a tool on this MCP server.

        Args:
            tool_name: Name of the tool to execute.
            **kwargs: Arguments to pass to the tool.

        Returns:
            The tool execution result.

        Raises:
            ValueError: If the tool is not found or arguments are invalid.
        """
        if tool_name == "get_repository":
            return self._get_repository(**kwargs)
        elif tool_name == "list_repository_files":
            return self._list_repository_files(**kwargs)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    def initialize(self) -> None:
        """Initialize the MCP client and connect to the server."""
        self._tools = {
            "get_repository": self._get_repository,
            "list_repository_files": self._list_repository_files,
        }

    def shutdown(self) -> None:
        """Shutdown the MCP client and clean up resources."""
        self._tools.clear()

    def _get_repository(self, **kwargs: Any) -> dict[str, Any]:
        """Get repository information.

        Args:
            owner: The repository owner (username or organization).
            repo: The repository name.

        Returns:
            Repository information dictionary.

        Raises:
            ValueError: If owner or repo is missing or invalid.
        """
        owner = kwargs.get("owner")
        repo = kwargs.get("repo")

        if owner is None:
            raise ValueError("Missing 'owner' argument. Provide a repository owner.")

        if repo is None:
            raise ValueError("Missing 'repo' argument. Provide a repository name.")

        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("The 'owner' argument must be a non-empty string.")

        if not isinstance(repo, str) or not repo.strip():
            raise ValueError("The 'repo' argument must be a non-empty string.")

        # Mock repository response
        return {
            "name": repo,
            "full_name": f"{owner}/{repo}",
            "owner": owner,
            "description": f"Mock repository: {owner}/{repo}",
            "url": f"https://github.com/{owner}/{repo}",
            "stars": 42,
            "forks": 10,
            "language": "Python",
            "mock": True,
            "provider": "github-mcp"
        }

    def _list_repository_files(self, **kwargs: Any) -> list[str]:
        """List files in a repository.

        Args:
            owner: The repository owner (username or organization).
            repo: The repository name.

        Returns:
            List of file paths in the repository.

        Raises:
            ValueError: If owner or repo is missing or invalid.
        """
        owner = kwargs.get("owner")
        repo = kwargs.get("repo")

        if owner is None:
            raise ValueError("Missing 'owner' argument. Provide a repository owner.")

        if repo is None:
            raise ValueError("Missing 'repo' argument. Provide a repository name.")

        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("The 'owner' argument must be a non-empty string.")

        if not isinstance(repo, str) or not repo.strip():
            raise ValueError("The 'repo' argument must be a non-empty string.")

        # Mock file listing
        return [
            f"{owner}/{repo}/README.md",
            f"{owner}/{repo}/src/main.py",
            f"{owner}/{repo}/src/utils.py",
            f"{owner}/{repo}/tests/test_main.py",
            f"{owner}/{repo}/pyproject.toml",
            f"{owner}/{repo}/docs/index.md"
        ]