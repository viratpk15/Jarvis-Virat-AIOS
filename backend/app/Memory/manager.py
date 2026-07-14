from app.Memory.storage import storage
from app.Memory.window import WindowManager, WindowedChatMessageHistory
from app.Memory.summarization import SummaryManager


# Window configuration
# Maximum number of messages to retain per session (must be even to preserve Human/AI pairs)
# 10 messages = 5 Human/AI pairs
WINDOW_SIZE: int = 10

# Summarization configuration
# Trigger summarization when total messages exceed this threshold
SUMMARIZATION_THRESHOLD: int = 20
# Number of recent messages to preserve when summarizing
SUMMARIZATION_KEEP_RECENT: int = 10


class MemoryManager:
    def __init__(self):
        """Initialize memory manager with window and summarization."""
        self._window_manager = WindowManager(window_size=WINDOW_SIZE)
        self._summary_manager = SummaryManager(
            threshold=SUMMARIZATION_THRESHOLD,
            keep_recent=SUMMARIZATION_KEEP_RECENT,
        )

    def get_conversation(self, session_id: str) -> WindowedChatMessageHistory:
        """Get conversation history for a session with window and summarization.

        Retrieves or creates a windowed chat message history for the given
        session. The window ensures only the most recent messages are
        returned while preserving complete Human/AI pairs. If the conversation
        exceeds the summarization threshold, older messages are automatically
        summarized.

        Args:
            session_id: Unique identifier for the conversation session.

        Returns:
            WindowedChatMessageHistory instance with automatic windowing and summarization.
        """
        # Get the underlying chat history from storage
        history = storage.get_memory(session_id)

        # Wrap it with windowing and summarization
        return WindowedChatMessageHistory(
            window_manager=self._window_manager,
            history=history,
            summary_manager=self._summary_manager,
        )


memory_manager = MemoryManager()
