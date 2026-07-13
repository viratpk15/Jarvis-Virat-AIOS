"""
Jarvis AIOS
--------------------
Tool Registry
"""

from typing import Dict

from app.Tools.tool import Tool


class ToolRegistry:
    """
    Stores every available tool.
    """

    def __init__(self):

        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):

        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:

        if name not in self._tools:
            raise ValueError(f"Tool '{name}' is not registered.")

        return self._tools[name]

    def list_tools(self):

        return list(self._tools.values())


registry = ToolRegistry()
