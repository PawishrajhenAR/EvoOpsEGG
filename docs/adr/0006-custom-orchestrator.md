# ADR 0006: Custom orchestrator

**Status:** Accepted  
**Date:** 2026-10-07

## Context

Task triage requires explicit steps: classify, retrieve, route tools, persist events, correlate traces, and respect tool policies. Off-the-shelf agent frameworks may obscure auditability or fight Supabase/Langfuse integration.

## Decision

Implement a **custom orchestrator** in `apps/api` that:

- Loads the **active** `agent_version` at `task_run` start and stores version id on the run.
- Executes a **declarative routing graph** from version config (not hardcoded per demo ticket).
- Emits **`run_events`** and **`tool_calls`** for every step.
- Integrates OpenAI for LLM steps and Langfuse for trace correlation.
- Enqueues long work (embeddings, eval batches) via **`jobs`**.

Third-party agent frameworks may be used as libraries but not as the sole source of truth for state or audit.

## Consequences

- **Positive:** Full control over gates, logging, and evolution snapshots.
- **Negative:** More in-house code to maintain; agent E owns core runtime.
- **Follow-ups:** Architecture doc details sync vs async paths when written.
