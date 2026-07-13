"""
Jarvis AIOS
--------------------
Tool Registry
"""

from typing import Dict

from app.Tools.tool import Tool
from app.Tools.calculator import CalculatorTool
from app.Tools.datetime_tool import DateTimeTool
from app.Tools.file_reader import FileReaderTool
from app.Tools.python_runner import PythonRunnerTool


class ToolRegistry:
    """
    Stores every available tool.
    """

    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

        # Register all available tools
        self.register(CalculatorTool())
        self.register(DateTimeTool())
        self.register(FileReaderTool())
        self.register(PythonRunnerTool())

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' is not registered.")

        return self._tools[name]

    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())


registry = ToolRegistry()
