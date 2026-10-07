# ADR 0009: Backend hosting not on Vercel (Python)

**Status:** Accepted  
**Date:** 2026-10-07

## Context

Vercel excels at Next.js but is not the primary target for long-running Python workers, background job consumers, and persistent FastAPI processes. EvoOps requires API + worker processes with Supabase service access.

## Decision

- **Next.js** → **Vercel** only.
- **FastAPI HTTP** and **background workers** → **Railway or Render** (either acceptable; pick one per environment for simplicity).
- Do not deploy Python API/worker to Vercel serverless functions in v1.

Workers poll/process `jobs` (embeddings, eval, notifications). HTTP service binds to platform `PORT` on `0.0.0.0`.

## Consequences

- **Positive:** Predictable worker semantics; simpler local parity.
- **Negative:** Two deploy pipelines; CORS and `NEXT_PUBLIC_API_URL` must stay aligned.
- **Follow-ups:** `docs/DEPLOYMENT.md`; agent L owns CI deploy steps.
