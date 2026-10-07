# EvoOps Deployment Guide

**Status:** Planning baseline  
**Owner:** DevOps Release agent (L)

EvoOps splits hosting by runtime: **Vercel** for the Next.js web app, **Railway or Render** for the Python API and background workers, and **Supabase** for Postgres, Auth, RLS, and pgvector. LLM, email, and observability are external SaaS APIs.

---

## 1. Environment matrix

| Environment | Purpose | Web | API / worker | Supabase | Data |
|-------------|---------|-----|--------------|----------|------|
| **local** | Developer machines | `localhost:3000` | `localhost:8000` | Local CLI or dev project | Seed / disposable |
| **staging** | Integration, TestSprite, eval | Vercel preview or staging project | Railway/Render staging service | Staging project | Anonymized fixtures |
| **prod** | Demo / live single-org | Vercel production | Railway/Render production | Production project | Real org data |

**Rule:** Staging must mirror prod topology (same env var *names*, different values). Never point local `.env` at production Supabase.

---

## 2. Component deployment map

```text
                    ┌─────────────────┐
                    │  Vercel (web)   │
                    │  apps/web       │
                    └────────┬────────┘
                             │ HTTPS
                             ▼
                    ┌─────────────────┐
                    │ Railway/Render  │
                    │ apps/api        │
                    │ + worker proc   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
  │  Supabase   │    │   OpenAI    │    │   Resend    │
  │  PG+Auth+   │    │             │    │             │
  │  pgvector   │    └─────────────┘    └─────────────┘
  └─────────────┘
         │
         ▼
  ┌─────────────┐    ┌─────────────┐
  │  Langfuse   │    │ TestSprite  │
  │  (traces)   │    │ (CI E2E)    │
  └─────────────┘    └─────────────┘
```

See [ADR 0009](adr/0009-backend-hosting-not-vercel-python.md) for why Python does not run on Vercel in v1.

---

## 3. Vercel (web)

**Project root:** `apps/web` (monorepo root directory setting in Vercel).

**Build:** Standard Next.js; set `NEXT_PUBLIC_*` for Supabase and public API URL.

**Required env vars (staging/prod):**

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `NEXT_PUBLIC_API_URL` → Railway/Render API base URL
- `NEXT_PUBLIC_APP_ENV` → `staging` | `production`

**Preview deployments:** Every PR branch gets a preview URL; TestSprite smoke targets staging or labeled preview.

**Binding:** Vercel manages edge/serverless; no manual `PORT` binding.

---

## 4. Railway / Render (API + worker)

**Services (recommended):**

1. **API** — FastAPI HTTP (`apps/api`), health check `/health`.
2. **Worker** — Same codebase, different start command (poll `jobs` table: embeddings, eval batches, retries).

**Platform notes:**

- **Render:** Bind HTTP to `0.0.0.0:$PORT` ([Render port binding](https://render.com/docs/web-services#port-binding)).
- **Railway:** Set `PORT` from platform; expose public URL for API.

**Required env vars:**

- `DATABASE_URL` or Supabase connection string (service role for workers only where needed)
- `SUPABASE_SERVICE_ROLE_KEY` (server-side only — never on Vercel client)
- `OPENAI_API_KEY`
- `RESEND_API_KEY`
- `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`
- `APP_ENV`, `CORS_ORIGINS` (include Vercel URLs)
- Connector secrets (Slack, etc.) as added

**Worker scaling:** Start with one worker instance; scale horizontally only after job locking is verified in migrations.

---

## 5. Supabase

**Responsibilities:** Auth (operator / approver / admin), Postgres schema, RLS, pgvector for ops RAG, optional Storage for knowledge uploads.

**Migrations:** `supabase/migrations/` applied via Supabase CLI in CI/CD before app deploy.

**Keys:**

- **Anon key** → web client only (RLS enforced).
- **Service role** → API/worker server-side only; never expose to browser.

**Branches (optional):** Use Supabase branching for preview DBs when available; otherwise single staging project.

---

## 6. External services

| Service | Config location | Notes |
|---------|-----------------|-------|
| OpenAI | API/worker env | Rate limits; log via Langfuse |
| Resend | API/worker env | Domain verification in Resend dashboard |
| Langfuse | API/worker env | Trace IDs correlated with `task_run` id |
| TestSprite | CI secrets | Staging base URL |
| Graphify | Developer machines | Outputs in `graphify-out/` (gitignored); optional `GRAPH_REPORT.md` at repo root |

---

## 7. Secrets management

1. **Never** commit `.env` or real keys ([`.env.example`](../.env.example) only).
2. **Vercel:** Project env vars per environment (Preview / Production).
3. **Railway/Render:** Secret env vars; separate staging vs prod services.
4. **Supabase:** Vault or encrypted connector refs in DB — not plaintext in `agent_versions` JSON.
5. **Rotation:** Document rotation in `audit_log`; redeploy API/worker after key rotation.

**CI:** GitHub Actions (or equivalent) secrets for `DATABASE_URL` (staging), `TESTSPRITE_*`, deploy tokens.

---

## 8. Deploy sequence (staging / prod)

1. Run DB migrations on target Supabase project.
2. Deploy API → wait for health check.
3. Deploy worker → verify job consumer heartbeat.
4. Deploy web on Vercel → verify `NEXT_PUBLIC_API_URL`.
5. Smoke: create task, view trace link, run eval smoke (if evolution release).
6. TestSprite smoke on staging URL.

**Rollback:**

- Web: Vercel instant rollback to prior deployment.
- API/worker: redeploy previous image/build.
- Agent behavior: promote prior `ACTIVE` `agent_version` (product rollback — not a code rollback).

---

## 9. Local development

1. Copy [`.env.example`](../.env.example) to `.env` (api) and `apps/web/.env.local`.
2. `supabase start` (when CLI configured) or use hosted dev project.
3. Run API, worker, and web per README (Phase 0 scaffold).

---

## 10. Related documents

- [ADR 0001](adr/0001-stack-selection.md), [0003](adr/0003-supabase-as-system-of-record.md), [0009](adr/0009-backend-hosting-not-vercel-python.md)
- [TESTING_STRATEGY.md](TESTING_STRATEGY.md) — CI and TestSprite targets
- [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) — branching and release gates
