"""
Jarvis AIOS
--------------------
Tool Engine

Single execution gate for all tool invocations.
Enforces input validation, tool name safety checks,
and provides clean security-focused error messages.
"""

from typing import Any

from app.Tools.registry import registry
from app.Observability.trace import measure_time, calculate_duration
from app.Observability.manager import observability_manager

# Maximum allowed length for a tool name string.
_MAX_TOOL_NAME_LENGTH: int = 64

# Maximum total size (in characters) for tool arguments JSON.
# Prevents resource exhaustion via oversized argument payloads.
_MAX_ARGUMENTS_CHARS: int = 100_000

# Allowed characters in tool names: alphanumeric, underscore, hyphen.
# Prevents injection through malformed tool name strings.
_ALLOWED_TOOL_NAME_CHARS: set[str] = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
)


def _validate_tool_name(tool_name: str) -> None:
    """Validate that a tool name is safe and well-formed.

    Rejects empty names, excessively long names, and names containing
    characters outside the allowed set. This prevents injection attacks
    that might attempt to manipulate internal state through malformed
    tool name strings.

    Args:
        tool_name: The tool name string to validate.

    Raises:
        ValueError: If the tool name is invalid or unsafe.
    """
    if not isinstance(tool_name, str):
        raise ValueError(
            "Tool name must be a string. "
            f"Received {type(tool_name).__name__}."
        )

    if not tool_name.strip():
        raise ValueError(
            "Tool name must not be empty."
        )

    if len(tool_name) > _MAX_TOOL_NAME_LENGTH:
        raise ValueError(
            f"Tool name too long. Maximum length is "
            f"{_MAX_TOOL_NAME_LENGTH} characters."
        )

    # Reject characters outside the safe set
    for char in tool_name:
        if char not in _ALLOWED_TOOL_NAME_CHARS:
            raise ValueError(
                f"Tool name contains unsafe character: "
                f"'{char}' (code point {ord(char)}). "
                "Only alphanumeric characters, underscores, "
                "and hyphens are allowed."
            )


def _validate_arguments(kwargs: dict[str, Any]) -> None:
    """Validate tool arguments for safety and size limits.

    Ensures arguments are a valid dict and do not exceed maximum
    total character size, preventing resource exhaustion attacks
    through oversized payloads.

    Args:
        kwargs: The tool arguments dict to validate.

    Raises:
        ValueError: If arguments are invalid or exceed size limits.
    """
    if not isinstance(kwargs, dict):
        raise ValueError(
            "Tool arguments must be a dictionary. "
            f"Received {type(kwargs).__name__}."
        )

    # Calculate approximate total character size of arguments
    total_chars = sum(
        len(str(key)) + len(str(value))
        for key, value in kwargs.items()
    )

    if total_chars > _MAX_ARGUMENTS_CHARS:
        raise ValueError(
            f"Tool arguments too large. Total size "
            f"({total_chars} characters) exceeds the maximum "
            f"of {_MAX_ARGUMENTS_CHARS} characters."
        )


class ToolEngine:
    """
    Single execution gate for all tool invocations.

    Validates tool names and arguments before delegation to the
    registry. Provides clean, security-focused error messages
    that do not leak internal implementation details.
    """

    def execute(
        self,
        tool_name: str,
        **kwargs: Any,
    ) -> Any:
        """Execute a tool by name with validated arguments.

        Tool names and arguments are validated for safety before
        any registry lookup or execution occurs. Invalid inputs
        are rejected with clear error messages.

        Args:
            tool_name: The registered name of the tool to execute.
            **kwargs: Arguments to pass to the tool.

        Returns:
            The result of the tool execution.

        Raises:
            ValueError: If the tool name or arguments are invalid,
                the tool is not registered, or execution fails.
        """
        # Validate inputs before any registry or tool interaction
        _validate_tool_name(tool_name)
        _validate_arguments(kwargs)

        # Look up the tool in the registry
        try:
            tool = registry.get(tool_name)
        except ValueError as e:
            raise ValueError(
                f"Tool '{tool_name}' is not available."
            ) from e

        # Execute the tool with validated arguments
        start_time = measure_time()
        try:
            result = tool.execute(**kwargs)
        except ValueError as e:
            # Re-raise tool-level validation errors as-is
            # (they are already clean security-focused messages)
            observability_manager.record_tool_call(
                tool_name=tool_name,
                duration_ms=calculate_duration(start_time),
                success=False,
                error=str(e),
            )
            raise
        except Exception:
            error_msg = (
                f"An error occurred while executing "
                f"the '{tool_name}' tool. Please check your "
                "inputs and try again."
            )
            observability_manager.record_tool_call(
                tool_name=tool_name,
                duration_ms=calculate_duration(start_time),
                success=False,
                error=error_msg,
            )
            raise ValueError(error_msg)
        else:
            observability_manager.record_tool_call(
                tool_name=tool_name,
                duration_ms=calculate_duration(start_time),
                success=True,
            )
            return result


engine = ToolEngine()
