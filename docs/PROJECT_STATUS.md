# EvoOps — Project Status

**Last updated:** Planning phase (pre-implementation)  
**Repository:** [EvoOpsEGG](https://github.com/PawishrajhenAR/EvoOpsEGG.git)  
**Implementation phase:** **Not started** (Phase 0 pending)

---

## Executive summary

Planning documentation for EvoOps is **complete** at the product, architecture, and data-model level. The repo contains **placeholder directories only** (`apps/web`, `apps/api`, `supabase/migrations`, `tests/unit`, `scripts`) with no application code, migrations, or CI workflows yet.

**Next gate:** Implement **Phase 0** (monorepo scaffold, baseline tooling, initial Supabase project wiring, and first authorized push policy acknowledgment).

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
| Next.js web app | ❌ Not started | Phase 0–1 |
| FastAPI service | ❌ Not started | Phase 0–2 |
| Supabase migrations & RLS | ❌ Not started | Phase 0–1 |
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
