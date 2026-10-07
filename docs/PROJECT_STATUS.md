# EvoOps — Project Status

**Last updated:** 2026-10-07 — Phase 1 auth foundation (local, not pushed)  
**Repository:** [EvoOpsEGG](https://github.com/PawishrajhenAR/EvoOpsEGG.git)  
**Implementation phase:** **Phase 1** — profiles/roles/RLS + login UI + API JWT gates

---

## Executive summary

Planning docs are complete. Phase 0 shells and **Phase 1 auth** (Supabase profiles/roles/RLS, web login, API JWT) are implemented locally on project **EvoOpsEGG**.

**Next gate:** Human test signup → bootstrap admin → role grants, then **Phase 2** (agent versions). Push only after explicit approval.

---

## What is done

| Area | Status | Notes |
|------|--------|-------|
| Product spec | ✅ Complete | [PRODUCT_SPEC.md](PRODUCT_SPEC.md) |
| Architecture | ✅ Complete | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Data model | ✅ Complete | [DATA_MODEL.md](DATA_MODEL.md) |
| Roadmap (Phases 0–14) | ✅ Complete | [ROADMAP.md](ROADMAP.md) |
| Root README | ✅ Complete | [../README.md](../README.md) |
| Locked decisions | ✅ Recorded | Single org; config-only evolution; stack per README |
| Git remote URL | ✅ Defined | `https://github.com/PawishrajhenAR/EvoOpsEGG.git` |

---

## What is not done

| Area | Status | Blocked by |
|------|--------|------------|
| Next.js web app | ✅ Phase 0 shell | `apps/web` — `npm run dev` → :3000 |
| FastAPI service | ✅ Phase 0 shell | `apps/api` — `/health` + OpenAPI; pytest green |
| Supabase migrations & RLS | ✅ Phase 1 | `profiles`, `roles`, `user_roles` + RLS + RPCs on EvoOpsEGG |
| Agent orchestrator | ❌ Not started | Phase 3+ |
| Ops RAG (pgvector) | ❌ Not started | Phase 4 |
| Tool connectors & policies | ❌ Not started | Phase 5 |
| Evolution & eval pipeline | ❌ Not started | Phase 8–9 |
| Approval & promotion flows | ❌ Not started | Phase 10 |
| Langfuse tracing | ❌ Not started | Phase 7 |
| Resend notifications | ❌ Not started | Phase 12 |
| TestSprite E2E | ❌ Not started | Phase 13 |
| Graphify (dev intel) | ✅ Bootstrapped | Cursor rule + AST graph on `apps/api/evoops` (101 nodes); docs semantic pass needs API key later |
| Staging & production envs | ❌ Not started | Phase 0 + hosting accounts |

---

## Repository inventory (current)

```
apps/web/          → .gitkeep only
apps/api/          → .gitkeep only
supabase/migrations/ → .gitkeep only
tests/unit/        → .gitkeep only
scripts/           → .gitkeep only
docs/              → planning markdown (this set)
README.md          → project entrypoint
```

No `package.json`, `pyproject.toml`, or `.github/workflows` yet.

---

## Risks & assumptions

| Item | Mitigation |
|------|------------|
| Eval flakiness with live LLM | Golden cases with tolerance bands; freeze model version in eval config |
| Tool side-effects in eval | Sandbox connectors or mock HTTP connector for eval runs |
| RLS complexity | Phase 1 delivers minimal policies; expand with feature phases |
| Scope creep into “self-modifying code” | Enforced in reviews: only `agent_versions.config` mutates via evolution |

---

## Push & release policy (reminder)

1. **First push** to GitHub is authorized to publish planning docs and Phase 0 scaffold when ready.
2. **Later pushes** require explicit human approval after testing (unit, eval where relevant, TestSprite for UI flows).

---

## How to update this document

After each phase completion:

1. Mark deliverables in the phase checklist in [ROADMAP.md](ROADMAP.md).
2. Update tables above (done / not done).
3. Set **Implementation phase** to the current phase number and date.

---

## Quick links

- [Roadmap](ROADMAP.md)
- [Architecture](ARCHITECTURE.md)
- [Data model](DATA_MODEL.md)
- [Product spec](PRODUCT_SPEC.md)
