# ADR 0003: Supabase as system of record

**Status:** Accepted  
**Date:** 2026-10-07

## Context

EvoOps persists tasks, agent versions, tool calls, knowledge chunks, eval runs, approvals, and audit events. Consistency, RLS, and pgvector for ops RAG are first-class requirements.

## Decision

**Supabase Postgres** is the **system of record** for all application entities. Supabase Auth issues JWTs for users; **RLS** enforces role-based access on all tenant tables. pgvector stores embeddings for `knowledge_chunks`.

- **Anon key + user JWT** on the web client only.
- **Service role** on API/workers for privileged operations, minimized and audited.
- Migrations live in `supabase/migrations/` and apply before app deploys.

## Consequences

- **Positive:** Single source of truth; built-in auth; vector colocated with relational data.
- **Negative:** Vendor coupling; service role misuse is a critical risk — mitigated by ADR 0008 and security agent J.
- **Follow-ups:** `DATA_MODEL.md` and migrations owned by agent B.
