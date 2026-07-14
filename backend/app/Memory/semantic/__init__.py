"""
Semantic Memory Subsystem

Provides semantic retrieval of relevant memories using cosine similarity.
Internal component of the Memory layer - accessed only through MemoryManager.
"""

from app.Memory.semantic.retriever import SemanticRetriever

__all__ = [
    "SemanticRetriever",
]