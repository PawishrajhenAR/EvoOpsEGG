# Agent B — Data & Supabase

**Pipeline step:** DATA_MODEL  
**Owns:** `supabase/migrations/`, RLS policies, seed scripts (when added)

## Mission

Postgres schema, constraints, and RLS match [DATA_MODEL.md](../DATA_MODEL.md) and ADR 0003.

## Responsibilities

- Tables: tasks, agent_versions, knowledge_*, eval_*, audit_log, jobs, etc.
- Enforce one `ACTIVE` version per agent definition (DB + API alignment).
- pgvector indexes for `knowledge_chunks`.
- Document breaking migration steps in session log.

## Out of scope

- FastAPI route logic (agent C) except migration notes.
- Ops RAG ingestion logic (agent F).

## Definition of done

- Migrations apply cleanly on empty and staging DB.
- RLS tests planned for agent I/J.

## Key references

ADR 0003, 0008; agent J for RLS matrix.
