"""
Jarvis AIOS
--------------------
File Reader Tool

Reads text files from an approved workspace directory only.
Arbitrary filesystem access and path traversal attacks are
prevented through strict path resolution, symlink checking,
and canonical path validation against the allowed directory.
"""

from pathlib import Path
from typing import Any

from app.Tools.tool import Tool

# The only directory from which files may be read.
# All paths are resolved and validated against this base.
# Change this via environment configuration in production.
_ALLOWED_DIRECTORY: Path = Path.cwd() / "workspace"


class FileReaderTool(Tool):
    name = "file_reader"

    description = "Reads text from a file."

    def execute(self, **kwargs: Any) -> Any:
        """Read a text file from the approved workspace directory.

        The path is resolved and validated to ensure it stays within
        the allowed directory. Directory traversal attacks using '..'
        or symlinks are blocked.

        Args:
            path: The file path relative to or within the allowed
                workspace directory.

        Returns:
            The file contents as a string.

        Raises:
            ValueError: If the path is missing, resolves outside the
                allowed directory, the file does not exist, or the
                file is too large.
        """
        path = kwargs.get("path")

        if not path:
            raise ValueError(
                "Missing 'path' argument. Provide a file path as a string."
            )

        if not isinstance(path, str) or not path.strip():
            raise ValueError(
                "The 'path' argument must be a non-empty string."
            )

        # Ensure the allowed directory exists
        try:
            _ALLOWED_DIRECTORY.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise ValueError(
                f"Cannot access workspace directory: {e}"
            ) from e

        # Resolve the allowed directory to its canonical absolute path
        try:
            allowed_resolved = _ALLOWED_DIRECTORY.resolve(strict=False)
        except (OSError, RuntimeError) as e:
            raise ValueError(
                f"Cannot resolve workspace directory: {e}"
            ) from e

        # Resolve the requested path to its canonical absolute path
        try:
            requested_path = (_ALLOWED_DIRECTORY / path).resolve(strict=False)
        except (OSError, RuntimeError) as e:
            raise ValueError(
                f"Invalid file path: {e}"
            ) from e

        # Block symlink traversal: if the resolved path has symlinks,
        # verify they point within the allowed directory
        # Part 1: Check if the requested path itself is a symlink pointing outside
        try:
            # Check immediate symlink (the final component)
            target_path = (_ALLOWED_DIRECTORY / path)
            if target_path.is_symlink():
                symlink_target = target_path.resolve(strict=False)
                try:
                    symlink_target.relative_to(allowed_resolved)
                except ValueError:
                    raise ValueError(
                        f"Access denied: '{path}' is a symlink that resolves "
                        f"outside the allowed workspace directory."
                    )
        except OSError:
            pass  # Not a symlink or inaccessible — proceed with normal checks

        # Part 2: Check that no component in the path is a symlink pointing outside
        try:
            # Walk path components from the allowed directory down
            current = allowed_resolved
            relative_parts = Path(path).parts
            for part in relative_parts:
                if part in ("..", "."):
                    raise ValueError(
                        "Access denied: Path must not contain '..' or '.' components."
                    )
                current = current / part
                if current.is_symlink():
                    symlink_target = current.resolve(strict=False)
                    try:
                        symlink_target.relative_to(allowed_resolved)
                    except ValueError:
                        raise ValueError(
                            f"Access denied: path component '{part}' is a symlink "
                            f"that resolves outside the allowed workspace directory."
                        )
        except OSError:
            pass  # Component inaccessible — will be caught by existence check below

        # Block directory traversal: resolved path must start with allowed directory
        try:
            requested_path.relative_to(allowed_resolved)
        except ValueError:
            raise ValueError(
                f"Access denied: '{path}' resolves outside the allowed workspace "
                f"directory. Path traversal is blocked."
            )

        # Check that the target exists and is a file
        if not requested_path.exists():
            raise ValueError(
                f"File not found at the specified path."
            )

        if not requested_path.is_file():
            raise ValueError(
                "The specified path is not a regular file."
            )

        # Check file size (limit: 1MB) to prevent memory exhaustion
        max_bytes: int = 1_000_000
        try:
            file_size = requested_path.stat().st_size
        except OSError as e:
            raise ValueError(f"Cannot access file: {e}") from e

        if file_size > max_bytes:
            raise ValueError(
                f"File too large. Maximum allowed size is "
                f"approximately 1 MB."
            )

        # Read the file contents
        try:
            return requested_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raise ValueError(
                "The file is not a valid UTF-8 text file. "
                "Binary files are not supported."
            )
        except OSError as e:
            raise ValueError(f"Failed to read file: {e}") from e
