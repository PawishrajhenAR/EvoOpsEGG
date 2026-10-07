# Agent F — Knowledge (ops RAG)

**Pipeline step:** IMPLEMENT  
**Owns:** Ingestion, chunking, embedding jobs, retrieval API used by orchestrator

## Mission

Curated ops runbooks in Supabase pgvector — **not** Graphify (ADR 0004).

## Responsibilities

- `knowledge_documents` / `knowledge_chunks` pipeline.
- Tag-based scoping and RLS-aware retrieval.
- Backfill embeddings via `jobs` worker.

## Out of scope

- Graphify reports (`graphify-out/`).
- Agent version config (H).

## Definition of done

- Retrieval quality measurable via eval cases (I).
- No cross-role document leakage in tests (J).

## Key references

ADR 0003, 0004; PRODUCT_SPEC §6.3.
