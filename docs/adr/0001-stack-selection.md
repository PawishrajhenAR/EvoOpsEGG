# ADR 0001: Stack selection

**Status:** Accepted  
**Date:** 2026-10-07

## Context

EvoOps needs a web console for operators and approvers, a durable backend for task orchestration and async jobs, vector search for ops runbooks, and integrations with LLM, email, and observability providers. The team is small and demo-driven; operational complexity must stay bounded.

## Decision

Adopt the following v1 stack:

| Layer | Choice |
|-------|--------|
| Web UI | Next.js, TypeScript, Tailwind on **Vercel** |
| API & workers | **FastAPI (Python)** on **Railway or Render** |
| Data & auth | **Supabase** (Postgres, Auth, RLS, pgvector) |
| LLM | OpenAI |
| Email | Resend |
| Observability | Langfuse |
| Engineering intel | Graphify (developer-only, not ops RAG) |
| E2E | TestSprite |

Single-organization tenancy; roles `operator`, `approver`, `admin`.

## Consequences

- **Positive:** Fast UI iteration on Vercel; Python ecosystem for agent/orchestration code; Supabase accelerates auth and RLS.
- **Negative:** Multi-host deployment (Vercel + Railway/Render + Supabase) requires clear env and CORS discipline.
- **Follow-ups:** ADR 0009 for Python hosting; deployment guide in `docs/DEPLOYMENT.md`.
