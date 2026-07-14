from langchain_core.messages import BaseMessage

from app.Memory.storage import storage
from app.Memory.window import WindowManager, WindowedChatMessageHistory
from app.Memory.summarization import SummaryManager
from app.Memory.persistence import SQLitePersistenceBackend
from app.Memory.embeddings import EmbeddingManager, LocalEmbeddingProvider
from app.Memory.semantic import SemanticRetriever


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

# Embedding configuration
# Whether to enable embedding generation
EMBEDDING_ENABLED: bool = True

# Semantic retrieval configuration
# Default similarity threshold for semantic retrieval (0-1)
SEMANTIC_SIMILARITY_THRESHOLD: float = 0.5


class MemoryManager:
    def __init__(self):
        """Initialize memory manager with window, summarization, persistence, and embeddings."""
        self._window_manager = WindowManager(window_size=WINDOW_SIZE)
        self._summary_manager = SummaryManager(
            threshold=SUMMARIZATION_THRESHOLD,
            keep_recent=SUMMARIZATION_KEEP_RECENT,
        )
        self._persistence = SQLitePersistenceBackend(db_path=PERSISTENCE_DB_PATH)
        self._hydrated_sessions: set[str] = set()  # Track hydrated sessions

        # Initialize embedding manager
        embedding_provider = LocalEmbeddingProvider()
        self._embedding_manager = EmbeddingManager(
            provider=embedding_provider,
            persistence=self._persistence if EMBEDDING_ENABLED else None,
            enabled=EMBEDDING_ENABLED,
        )

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

        # Wrap it with windowing, summarization, persistence, and embeddings
        return WindowedChatMessageHistory(
            window_manager=self._window_manager,
            history=history,
            summary_manager=self._summary_manager,
            persistence=self._persistence,
            session_id=session_id,
            summary=summary,
            embedding_manager=self._embedding_manager,
        )

    def get_relevant_memories(
        self,
        session_id: str,
        query: str,
        top_k: int = 5,
    ) -> list[BaseMessage]:
        """Retrieve relevant memories using semantic similarity.

        Uses the SemanticRetriever to find messages whose embeddings are
        most similar to the query. This is the ONLY public interface for
        semantic memory retrieval.

        Args:
            session_id: Unique session identifier.
            query: User query to find relevant memories for.
            top_k: Maximum number of messages to return. Defaults to 5.

        Returns:
            List of BaseMessage objects ranked by similarity (highest first).
            Returns empty list if no messages meet the threshold or if
            embeddings are not enabled.
        """
        retriever = SemanticRetriever(
            embedding_manager=self._embedding_manager,
            persistence=self._persistence,
            similarity_threshold=SEMANTIC_SIMILARITY_THRESHOLD,
        )

        return retriever.retrieve(
            session_id=session_id,
            query=query,
            top_k=top_k,
        )


memory_manager = MemoryManager()
