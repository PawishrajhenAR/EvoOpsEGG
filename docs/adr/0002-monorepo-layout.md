# ADR 0002: Monorepo layout

**Status:** Accepted  
**Date:** 2026-10-07

## Context

EvoOps ships a web app, API, workers, database migrations, and shared tests. Split repositories would slow coordinated changes (schema + API + UI) during the evolution demo loop.

## Decision

Use a **single repository** with top-level layout:

```text
apps/web/          # Next.js
apps/api/          # FastAPI (+ worker entrypoint)
supabase/migrations/
tests/unit/        # (+ integration, e2e as added)
scripts/
docs/
```

Package managers may differ per app (`pnpm` for web, `uv`/`poetry`/`pip` for api — chosen in Phase 0 scaffold). Shared types cross via OpenAPI/codegen or documented contracts, not a shared npm package in v1 unless needed.

## Consequences

- **Positive:** One PR can land vertical slices; agents have clear path ownership.
- **Negative:** CI must path-filter jobs (web vs api vs supabase).
- **Follow-ups:** Phase 0 scaffold; agent contracts C, D, B for owned trees.
