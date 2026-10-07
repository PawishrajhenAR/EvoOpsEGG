# Agent C — API (FastAPI)

**Pipeline step:** IMPLEMENT  
**Owns:** `apps/api/` HTTP layer, OpenAPI, auth middleware

## Mission

Expose REST (or RPC) endpoints for tasks, agents, evolution, eval triggers, admin — backed by Supabase with correct JWT/service role usage.

## Responsibilities

- Health checks, CORS, error envelopes.
- Map domain services from orchestrator (E) and evolution (H).
- Never expose `SUPABASE_SERVICE_ROLE_KEY` to web.

## Out of scope

- Next.js UI (D); worker loop details shared with L.

## Definition of done

- OpenAPI documents public contracts.
- Integration tests for critical routes (with I).

## Key references

ADR 0006, 0009; [DEPLOYMENT.md](../DEPLOYMENT.md).
