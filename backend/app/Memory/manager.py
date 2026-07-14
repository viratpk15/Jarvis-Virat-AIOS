from app.Memory.storage import storage
from app.Memory.window import WindowManager, WindowedChatMessageHistory
from app.Memory.summarization import SummaryManager
from app.Memory.persistence import SQLitePersistenceBackend


# Window configuration
# Maximum number of messages to retain per session (must be even to preserve Human/AI pairs)
# 10 messages = 5 Human/AI pairs
WINDOW_SIZE: int = 10

# Summarization configuration
# Trigger summarization when total messages exceed this threshold
SUMMARIZATION_THRESHOLD: int = 20
# Number of recent messages to preserve when summarizing
SUMMARIZATION_KEEP_RECENT: int = 10

# Persistence configuration
# Path to SQLite database for persistent memory
PERSISTENCE_DB_PATH: str = "./data/memory.db"


class MemoryManager:
    def __init__(self):
        """Initialize memory manager with window, summarization, and persistence."""
        self._window_manager = WindowManager(window_size=WINDOW_SIZE)
        self._summary_manager = SummaryManager(
            threshold=SUMMARIZATION_THRESHOLD,
            keep_recent=SUMMARIZATION_KEEP_RECENT,
        )
        self._persistence = SQLitePersistenceBackend(db_path=PERSISTENCE_DB_PATH)
        self._hydrated_sessions: set[str] = set()  # Track hydrated sessions

    def get_conversation(self, session_id: str) -> WindowedChatMessageHistory:
        """Get conversation history for a session with window, summarization, and persistence.

        Retrieves or creates a windowed chat message history for the given
        session. If a persisted session exists and hasn't been hydrated yet,
        it is loaded from SQLite exactly once. The window ensures only the
        most recent messages are returned while preserving complete Human/AI
        pairs. If the conversation exceeds the summarization threshold, older
        messages are automatically summarized.

        Args:
            session_id: Unique identifier for the conversation session.

        Returns:
            WindowedChatMessageHistory instance with automatic windowing, summarization, and persistence.
        """
        # Get the underlying chat history from storage
        history = storage.get_memory(session_id)

        # Load persisted session data only if not already hydrated
        # This prevents duplicate message loading on subsequent calls
        if session_id not in self._hydrated_sessions:
            persisted_data = self._persistence.load_session(session_id)
            if persisted_data:
                # Restore summary
                summary = persisted_data.get("summary")
                # Restore messages
                persisted_messages = persisted_data.get("messages", [])
                for msg in persisted_messages:
                    history.add_message(msg)
            else:
                summary = None

            # Mark as hydrated to prevent reloading
            self._hydrated_sessions.add(session_id)
        else:
            # Already hydrated, get summary from persistence if needed
            summary = self._persistence.load_summary(session_id)

        # Wrap it with windowing, summarization, and persistence
        return WindowedChatMessageHistory(
            window_manager=self._window_manager,
            history=history,
            summary_manager=self._summary_manager,
            persistence=self._persistence,
            session_id=session_id,
            summary=summary,
        )


memory_manager = MemoryManager()
