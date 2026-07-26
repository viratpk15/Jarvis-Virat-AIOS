"""
Jarvis AIOS — RAG Studio Repository Layer
"""

from typing import List, Optional, Dict
from app.RAG.models import (
    KnowledgeBase,
    Dataset,
    Document,
    Chunk,
    Embedding,
    RetrievalTrace,
    RAGEvaluation,
    KnowledgeGraphData,
)


class RAGRepository:
    def __init__(self):
        self._kbs: Dict[str, KnowledgeBase] = {}
        self._datasets: Dict[str, Dataset] = {}
        self._documents: Dict[str, Document] = {}
        self._chunks: Dict[str, Chunk] = {}
        self._embeddings: Dict[str, Embedding] = {}
        self._traces: List[RetrievalTrace] = []
        self._evaluations: List[RAGEvaluation] = []
        self._seed_default_data()

    def _seed_default_data(self):
        kb = KnowledgeBase(
            id="kb_enterprise_01",
            name="Enterprise Architecture KB",
            description="Production documentation and architectural constitutional rules.",
            default_embedding_model="text-embedding-3-small",
        )
        self._kbs[kb.id] = kb

        ds = Dataset(
            id="ds_core_docs",
            kb_id=kb.id,
            name="Core Architecture Docs",
            document_count=2,
        )
        self._datasets[ds.id] = ds

        doc1 = Document(
            id="doc_arch_01",
            dataset_id=ds.id,
            filename="02_ARCHITECTURE.md",
            file_type="md",
            file_size_bytes=14200,
            storage_path="docs/02_ARCHITECTURE.md",
        )
        doc2 = Document(
            id="doc_tools_02",
            dataset_id=ds.id,
            filename="05_TOOL_ENGINE.md",
            file_type="md",
            file_size_bytes=9800,
            storage_path="docs/05_TOOL_ENGINE.md",
        )
        self._documents[doc1.id] = doc1
        self._documents[doc2.id] = doc2

        # Seed sample chunks
        chk1 = Chunk(
            id="chk_arch_01",
            document_id=doc1.id,
            chunk_index=0,
            raw_text="Jarvis AIOS runtime orchestrates LangGraph execution nodes and ToolEngine tool invocations.",
            token_length=18,
            metadata_payload={"section": "Core Topology"},
        )
        chk2 = Chunk(
            id="chk_arch_02",
            document_id=doc1.id,
            chunk_index=1,
            raw_text="Vector embeddings are stored in ChromaDB HNSW index and pgvector for sub-10ms similarity search.",
            token_length=22,
            metadata_payload={"section": "Vector Storage"},
        )
        chk3 = Chunk(
            id="chk_tools_01",
            document_id=doc2.id,
            chunk_index=0,
            raw_text="ToolEngine validates tool parameters against JSON schema before execution.",
            token_length=15,
            metadata_payload={"section": "Tool Execution"},
        )
        self._chunks[chk1.id] = chk1
        self._chunks[chk2.id] = chk2
        self._chunks[chk3.id] = chk3

    def list_knowledge_bases(self) -> List[KnowledgeBase]:
        return list(self._kbs.values())

    def get_knowledge_base(self, kb_id: str) -> Optional[KnowledgeBase]:
        return self._kbs.get(kb_id)

    def create_knowledge_base(self, name: str, description: str = "") -> KnowledgeBase:
        kb = KnowledgeBase(name=name, description=description)
        self._kbs[kb.id] = kb
        return kb

    def list_datasets(self, kb_id: Optional[str] = None) -> List[Dataset]:
        if kb_id:
            return [d for d in self._datasets.values() if d.kb_id == kb_id]
        return list(self._datasets.values())

    def create_dataset(self, kb_id: str, name: str) -> Dataset:
        ds = Dataset(kb_id=kb_id, name=name)
        self._datasets[ds.id] = ds
        return ds

    def list_documents(self, dataset_id: Optional[str] = None) -> List[Document]:
        if dataset_id:
            return [d for d in self._documents.values() if d.dataset_id == dataset_id]
        return list(self._documents.values())

    def add_document(self, dataset_id: str, filename: str, file_type: str, raw_text: str) -> Document:
        doc = Document(
            dataset_id=dataset_id,
            filename=filename,
            file_type=file_type,
            file_size_bytes=len(raw_text.encode("utf-8")),
        )
        self._documents[doc.id] = doc

        # Simple auto-chunking
        words = raw_text.split()
        chunk_size = 50
        for i in range(0, max(1, len(words)), chunk_size):
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join(chunk_words)
            chunk = Chunk(
                document_id=doc.id,
                chunk_index=len(self._chunks),
                raw_text=chunk_text,
                token_length=len(chunk_words),
            )
            self._chunks[chunk.id] = chunk

        # Update dataset doc count
        if dataset_id in self._datasets:
            self._datasets[dataset_id].document_count += 1

        return doc

    def list_chunks(self, document_id: Optional[str] = None) -> List[Chunk]:
        if document_id:
            return [c for c in self._chunks.values() if c.document_id == document_id]
        return list(self._chunks.values())

    def add_trace(self, trace: RetrievalTrace):
        self._traces.append(trace)

    def list_traces(self) -> List[RetrievalTrace]:
        return self._traces

    def add_evaluation(self, eval_data: RAGEvaluation):
        self._evaluations.append(eval_data)

    def list_evaluations(self) -> List[RAGEvaluation]:
        return self._evaluations

    def get_knowledge_graph(self, kb_id: str) -> KnowledgeGraphData:
        nodes = [
            {"id": "Jarvis_AIOS", "label": "Jarvis AIOS", "category": "System"},
            {"id": "LangGraph", "label": "LangGraph Engine", "category": "Orchestrator"},
            {"id": "RAG_Subsystem", "label": "RAG Subsystem", "category": "Module"},
            {"id": "ChromaDB", "label": "ChromaDB Vector Store", "category": "Storage"},
            {"id": "ToolEngine", "label": "Tool Engine", "category": "Executor"},
        ]
        edges = [
            {"source": "Jarvis_AIOS", "target": "LangGraph", "relation": "uses"},
            {"source": "Jarvis_AIOS", "target": "RAG_Subsystem", "relation": "includes"},
            {"source": "RAG_Subsystem", "target": "ChromaDB", "relation": "indexes into"},
            {"source": "LangGraph", "target": "ToolEngine", "relation": "invokes"},
        ]
        return KnowledgeGraphData(kb_id=kb_id, nodes=nodes, edges=edges)
