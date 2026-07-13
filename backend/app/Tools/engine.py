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

        tool = registry.get(tool_name)

        return tool.execute(**kwargs)


engine = ToolEngine()
