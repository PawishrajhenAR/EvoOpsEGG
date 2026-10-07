# ADR 0004: Graphify for engineering intelligence, not ops RAG

**Status:** Accepted  
**Date:** 2026-10-07

## Context

EvoOps has two distinct knowledge needs: (1) **runtime ops runbooks** for ticket triage, and (2) **repository/engineering context** for developers building the platform. Conflating them risks wrong retrieval at runtime and unclear data governance.

## Decision

- **Ops RAG** at runtime uses Supabase `knowledge_documents` / `knowledge_chunks` (curated runbooks, policies).
- **Graphify** is used only for **engineering intelligence** (codebase graph, refactors, agent sessions building EvoOps).
- Graphify outputs default to `graphify-out/` (gitignored). **`GRAPH_REPORT.md`** at repo root may be committed optionally for human-readable summaries.

Graphify is **not** wired into the ticket triage retrieval path in v1.

## Consequences

- **Positive:** Clear boundary for demos; ops knowledge stays approver-curated.
- **Negative:** Two tooling surfaces for contributors — documented in README and PRODUCT_SPEC.
- **Follow-ups:** Do not add Graphify connector to production tool policies without a new ADR.
