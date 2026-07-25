"""
Jarvis AIOS
--------------------
Central LLM Client

Exposes a provider-independent LLM client abstraction shielding higher-level
modules (Runtime, LangGraph) from provider-specific SDKs (Groq, OpenAI, Gemini, etc.).
"""

import os
from typing import Any, Generator

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class LLMClient:
    """Provider-independent LLM client interface."""

    def __init__(self, provider: Any = None) -> None:
        """Initialize the LLM client with a provider instance.

        Defaults to ChatGroq using environment configuration.
        """
        self._provider = provider or ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
        )

    @property
    def provider(self) -> Any:
        """Get the underlying provider instance."""
        return self._provider

    def invoke(self, input_data: Any, **kwargs: Any) -> Any:
        """Synchronously invoke the LLM provider.

        Args:
            input_data: Prompt messages or input data.
            **kwargs: Additional provider-specific keyword arguments.

        Returns:
            Provider response object (e.g. AIMessage).
        """
        return self._provider.invoke(input_data, **kwargs)

    def stream(self, input_data: Any, **kwargs: Any) -> Generator[str, None, None]:
        """Stream token strings from the LLM provider in a provider-agnostic manner.

        Args:
            input_data: Prompt messages or input data.
            **kwargs: Additional provider-specific keyword arguments.

        Yields:
            Token string chunks as emitted by the underlying provider.
        """
        for chunk in self._provider.stream(input_data, **kwargs):
            token = getattr(chunk, "content", None)
            if token is None:
                token = str(chunk)
            if token:
                yield str(token)


llm_client = LLMClient()
llm = llm_client.provider

