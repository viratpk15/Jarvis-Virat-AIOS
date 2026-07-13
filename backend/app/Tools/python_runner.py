"""
Jarvis AIOS
--------------------
Python Runner Tool
"""

from contextlib import redirect_stdout
from io import StringIO
from typing import Any

from app.Tools.tool import Tool


class PythonRunnerTool(Tool):
    name = "python"

    description = "Executes Python code."

    def execute(self, **kwargs: Any) -> Any:

        code = kwargs.get("code")

        if not code:
            raise ValueError("Missing code.")

        output = StringIO()

        with redirect_stdout(output):
            exec(code, {}, {})

        return output.getvalue()
