"""
Jarvis AIOS
--------------------
Base Tool Interface
"""

from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):
    """
    Every Jarvis tool must inherit from this class.
    """

    name: str = ""
    description: str = ""

    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """
        Execute the tool.
        """
        raise NotImplementedError
