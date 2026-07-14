"""
Windowed Chat Message History

Wraps InMemoryChatMessageHistory to automatically apply sliding window
management, ensuring conversation history never exceeds the configured
size while preserving complete Human/AI pairs.
"""

from typing import TYPE_CHECKING

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory

if TYPE_CHECKING:
    from app.Memory.window.window_manager import WindowManager
    from app.Memory.summarization.summary_manager import SummaryManager


class WindowedChatMessageHistory:
    """Chat message history with automatic windowing and summarization.

    Wraps InMemoryChatMessageHistory and applies sliding window management
    and automatic summarization to prevent unbounded growth. The window is
    applied when messages are retrieved, ensuring only the most recent
    complete Human/AI pairs are returned. If the conversation exceeds the
    summarization threshold, older messages are automatically summarized.

    Attributes:
        window_manager: WindowManager instance that controls windowing.
        summary_manager: SummaryManager instance for summarization.
    """

    def __init__(
        self,
        window_manager: "WindowManager",
        history: InMemoryChatMessageHistory | None = None,
        summary_manager: "SummaryManager | None" = None,
    ):
        """Initialize windowed chat history.

        Args:
            window_manager: WindowManager instance that controls windowing.
            history: Optional existing chat history to wrap. If None, creates new.
            summary_manager: Optional SummaryManager for automatic summarization.
        """
        self._history = history if history is not None else InMemoryChatMessageHistory()
        self._window_manager = window_manager
        self._summary_manager = summary_manager
        self._summary: str | None = None  # Stores the conversation summary

    @property
    def messages(self) -> list[BaseMessage]:
        """Get windowed messages with optional summary.

        Returns messages with the following structure:
        1. Summary SystemMessage (if summary exists)
        2. Windowed recent messages

        Returns:
            List of messages ready for LLM consumption.
        """
        result: list[BaseMessage] = []

        # Add summary if it exists
        if self._summary:
            result.append(
                SystemMessage(content=f"Conversation Summary: {self._summary}")
            )

        # Apply windowing to recent messages
        all_messages = self._history.messages
        result.extend(self._window_manager.apply_window(all_messages))

        return result

    def add_message(self, message: BaseMessage) -> None:
        """Add a message to the history with event-driven summarization.

        Messages are added to the underlying history. If summarization is
        enabled and the threshold is crossed, older messages are automatically
        summarized and removed, leaving only the summary and recent messages.

        Args:
            message: Message to add to history.
        """
        # Add the new message
        self._history.add_message(message)

        # Check if summarization is needed (event-driven, not request-driven)
        if self._summary_manager and self._summary_manager.should_summarize(
            len(self._history.messages)
        ):
            self._perform_summarization()

    def _perform_summarization(self) -> None:
        """Perform summarization of older messages.

        This is called automatically when the message count exceeds the threshold.
        If a previous summary exists, it is merged with older messages to create
        an updated summary representing the entire conversation history so far.
        Summarizes older messages, stores the summary, and removes old messages.
        """
        all_messages = self._history.messages

        # Split into older and recent messages
        older_messages = self._summary_manager.get_messages_to_summarize(all_messages)
        recent_messages = self._summary_manager.get_recent_messages(all_messages)

        if not older_messages:
            return

        # If a previous summary exists, include it in the summarization
        # This ensures incremental summarization - the new summary represents
        # the entire conversation history, not just the latest batch
        if self._summary:
            # Create a SystemMessage from the previous summary
            from langchain_core.messages import SystemMessage
            previous_summary_msg = SystemMessage(
                content=f"Previous Conversation Summary: {self._summary}"
            )
            # Prepend the previous summary to older messages
            older_messages = [previous_summary_msg] + older_messages

        # Generate summary from older messages (including previous summary if exists)
        summary = self._summary_manager.summarize(older_messages)

        # Store the updated summary
        self._summary = summary

        # Clear history and keep only recent messages
        self._history.clear()
        for msg in recent_messages:
            self._history.add_message(msg)

    def clear(self) -> None:
        """Clear all messages from history."""
        self._history.clear()

    def __len__(self) -> int:
        """Get total message count (before windowing)."""
        return len(self._history.messages)
