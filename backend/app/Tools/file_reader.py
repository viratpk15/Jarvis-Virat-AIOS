"""
Jarvis AIOS
--------------------
File Reader Tool
"""

from pathlib import Path
from typing import Any

from app.Tools.tool import Tool


class FileReaderTool(Tool):
    name = "file_reader"

    description = "Reads text from a file."

    def execute(self, **kwargs: Any) -> Any:

        path = kwargs.get("path")

        if not path:
            raise ValueError("Missing file path.")

        return Path(path).read_text(encoding="utf-8")
