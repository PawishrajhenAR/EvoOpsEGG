"""Company knowledge retrieval — Postgres + pgvector (not Graphify)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RetrievedChunk:
    chunk_id: str
    document_id: str
    text: str
    score: float
    source_uri: str


class Retriever:
    """Hybrid search over runbooks and FAQs for the Ops Agent."""

    def search(self, query: str, top_k: int = 8) -> list[RetrievedChunk]:
        raise NotImplementedError("Phase 5")


class IngestWorker:
    """Chunk and embed uploaded documents into knowledge_chunks."""

    def ingest_document(self, document_id: str) -> int:
        raise NotImplementedError("Phase 5")
