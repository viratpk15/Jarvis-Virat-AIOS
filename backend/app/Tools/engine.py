"""
Jarvis AIOS
--------------------
Tool Engine
"""

from typing import Any

from app.Tools.registry import registry


class ToolEngine:
    """
    Executes registered tools.
    """

    def execute(
        self,
        tool_name: str,
        **kwargs: Any,
    ) -> Any:
        """Execute a tool by name with the given arguments.

        Args:
            tool_name: The registered name of the tool to execute.
            **kwargs: Arguments to pass to the tool.

        Returns:
            The result of the tool execution.

        Raises:
            ValueError: If the tool is not registered or execution fails.
        """
        try:
            tool = registry.get(tool_name)
        except ValueError as e:
            raise ValueError(f"Tool execution failed: {e}") from e

        try:
            return tool.execute(**kwargs)
        except Exception as e:
            raise ValueError(
                f"Tool execution failed for '{tool_name}': {e}"
            ) from e


engine = ToolEngine()
