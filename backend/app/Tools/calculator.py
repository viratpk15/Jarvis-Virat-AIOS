"""
Jarvis AIOS
--------------------
Calculator Tool
"""

from typing import Any

from app.Tools.tool import Tool


class CalculatorTool(Tool):
    name = "calculator"

    description = "Performs mathematical calculations."

    def execute(self, **kwargs: Any) -> Any:

        expression = kwargs.get("expression")

        if expression is None:
            raise ValueError("Missing 'expression' argument.")

        try:
            return eval(expression, {"__builtins__": {}}, {})
        except Exception as e:
            raise ValueError(f"Calculation failed: {e}")
