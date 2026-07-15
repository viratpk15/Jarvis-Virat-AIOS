"""
Jarvis AIOS
-----------
Filesystem MCP Server

Read-only filesystem access through the Model Context Protocol.
Provides secure list_directory and read_file tools with workspace
directory containment.
"""

from pathlib import Path
from typing import Any

from app.MCP.client import MCPClient, MCPServerConfig


# The only directory from which files may be accessed.
_ALLOWED_DIRECTORY: Path = Path.cwd() / "workspace"

# Maximum file size in bytes (1 MB).
_MAX_FILE_SIZE_BYTES: int = 1_000_000


def _validate_path_safety(path: str, allowed_dir: Path) -> Path:
    """Validate a file path and return its canonical, safe form.

    Security checks performed in order:
    1. Reject '..' and '.' path components explicitly.
    2. Reject absolute paths — all paths must be workspace-relative.
    3. Resolve the joined path to its canonical form via resolve(),
       which normalizes '..'/'.' and follows symlinks.
    4. Verify the canonical path is contained within the allowed
       directory.

    Args:
        path: The user-provided file path string.
        allowed_dir: The resolved canonical Path of the allowed
            workspace directory.

    Returns:
        A resolved, canonical Path guaranteed to be within the
        allowed directory.

    Raises:
        ValueError: If the path is unsafe for any reason.
    """
    # Step 1: Reject explicit '..' and '.' path components
    parts = Path(path).parts
    for part in parts:
        if part == "..":
            raise ValueError(
                "Path must not contain '..'. Directory traversal is not allowed."
            )
        if part == ".":
            raise ValueError("Path must not contain '.' components.")

    # Step 2: Reject absolute paths
    if Path(path).is_absolute():
        raise ValueError(
            "Absolute paths are not allowed. "
            "Provide a relative path within the workspace directory."
        )

    # Step 3: Join with the allowed directory and resolve to canonical form.
    try:
        resolved_path = (allowed_dir / path).resolve(strict=False)
    except (OSError, RuntimeError) as e:
        raise ValueError(f"Invalid file path: {e}") from e

    # Step 4: Verify the resolved canonical path is within the allowed directory.
    try:
        resolved_path.relative_to(allowed_dir)
    except ValueError:
        raise ValueError(
            "Access denied: the resolved path is outside "
            "the allowed workspace directory."
        )

    return resolved_path


class FilesystemMCPClient(MCPClient):
    """Filesystem MCP server with read-only access.

    Provides list_directory and read_file tools for browsing the
    workspace directory, with strict path validation to prevent
    directory traversal attacks.
    """

    def __init__(self, config: MCPServerConfig | None = None) -> None:
        """Initialize the Filesystem MCP client.

        Args:
            config: Optional MCP server configuration. If not provided,
                a default configuration is used.
        """
        self._config = config or MCPServerConfig(
            name="filesystem",
            description="Read-only filesystem access for workspace directory.",
            enabled=True,
            capabilities=["list_directory", "read_file"]
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
        if tool_name == "list_directory":
            return self._list_directory(**kwargs)
        elif tool_name == "read_file":
            return self._read_file(**kwargs)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    def initialize(self) -> None:
        """Initialize the MCP client and connect to the server.

        Creates the tools dictionary and ensures workspace directory exists.
        """
        self._tools = {
            "list_directory": self._list_directory,
            "read_file": self._read_file,
        }

    def shutdown(self) -> None:
        """Shutdown the MCP client and clean up resources."""
        self._tools.clear()

    def _list_directory(self, **kwargs: Any) -> list[str]:
        """List contents of a directory in the workspace.

        Args:
            path: Optional relative path within workspace. Defaults to root.

        Returns:
            List of entry names in the directory.

        Raises:
            ValueError: If path is invalid or directory doesn't exist.
        """
        # Ensure workspace directory exists
        try:
            allowed_resolved = _ALLOWED_DIRECTORY.resolve(strict=False)
            _ALLOWED_DIRECTORY.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise ValueError(f"Cannot access workspace directory: {e}") from e

        # Get optional path parameter
        path = kwargs.get("path", "")
        if path is None:
            path = ""

        if not isinstance(path, str):
            raise ValueError("The 'path' argument must be a string.")

        # Validate path safety
        if path.strip():
            requested_path = _validate_path_safety(path, allowed_resolved)
        else:
            requested_path = allowed_resolved

        # Check if directory exists
        if not requested_path.exists():
            raise ValueError("Directory not found at the specified path.")

        if not requested_path.is_dir():
            raise ValueError("The specified path is not a directory.")

        # List directory contents
        try:
            return sorted([entry.name for entry in requested_path.iterdir()])
        except OSError as e:
            raise ValueError(f"Failed to list directory: {e}") from e

    def _read_file(self, **kwargs: Any) -> str:
        """Read a text file from the workspace directory.

        Args:
            path: Relative path to the file within workspace.

        Returns:
            The file contents as a string.

        Raises:
            ValueError: If path is invalid, file doesn't exist, or
                file is too large or not valid UTF-8.
        """
        # Ensure workspace directory exists
        try:
            allowed_resolved = _ALLOWED_DIRECTORY.resolve(strict=False)
            _ALLOWED_DIRECTORY.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise ValueError(f"Cannot access workspace directory: {e}") from e

        path = kwargs.get("path")

        if path is None:
            raise ValueError(
                "Missing 'path' argument. Provide a file path as a string."
            )

        if not isinstance(path, str):
            raise ValueError("The 'path' argument must be a string.")

        if not path.strip():
            raise ValueError("The 'path' argument must be a non-empty string.")

        # Validate path safety
        requested_path = _validate_path_safety(path, allowed_resolved)

        # Check if file exists and is a file
        if not requested_path.exists():
            raise ValueError("File not found at the specified path.")

        if not requested_path.is_file():
            raise ValueError("The specified path is not a regular file.")

        # Check file size
        try:
            file_size = requested_path.stat().st_size
        except OSError as e:
            raise ValueError(f"Cannot access file: {e}") from e

        if file_size > _MAX_FILE_SIZE_BYTES:
            raise ValueError(
                "File too large. Maximum allowed size is approximately 1 MB."
            )

        # Read and return file contents
        try:
            return requested_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raise ValueError(
                "The file is not a valid UTF-8 text file. "
                "Binary files are not supported."
            )
        except OSError as e:
            raise ValueError(f"Failed to read file: {e}") from e