# EvoOps Testing Strategy

**Status:** Planning baseline (Phase 0+)  
**Owner:** Eval & Quality agent (I) with DevOps Release (L)

This document defines how EvoOps validates correctness at multiple layers: fast unit tests, integration tests against Supabase and the API, agent **eval datasets** (golden tasks), **security** checks, and **TestSprite** MCP-driven E2E for the operator/approver UI.

---

## 1. Testing pyramid

| Layer | Scope | Speed | When it runs |
|-------|--------|-------|--------------|
| **Unit** | Pure domain logic, config diffing, state machine transitions, policy evaluation | Seconds | Every PR, pre-commit optional |
| **Integration** | FastAPI routes + Supabase (local or ephemeral DB), RLS smoke, job enqueue | Minutes | Every PR |
| **Eval (agent config)** | `eval_suites` / `eval_cases` against **draft** `agent_versions` | Minutes–tens of minutes | PRs touching orchestration/evolution; required before `PENDING_APPROVAL` |
| **Security** | AuthZ matrix, RLS regression, secret scanning, tool-policy deny defaults | Minutes | Every PR; deeper scan on `main` |
| **E2E (TestSprite)** | Critical UI flows on staging | Tens of minutes | PRs with `apps/web` changes; nightly on `main` |

---

## 2. Unit tests

**Location:** `tests/unit/` (API/domain), `apps/web/**/*.test.ts(x)` when scaffold exists.

**Focus:**

- Agent version state machine (`DRAFT` → … → `ACTIVE`, failure paths).
- Evolution proposal diff application (config-only; no source mutation).
- Tool policy allow/deny and approval-required flags.
- Classification/routing helpers with frozen fixtures (no live LLM in unit tests).

**Conventions:**

- Mock OpenAI and external connectors at boundaries.
- Use deterministic seeds for any stochastic helpers.
- Target ≥80% line coverage on `apps/api` domain packages before demo-ready (Phase 10+).

---

## 3. Integration tests

**Location:** `tests/integration/` (to be added in Phase 0+).

**Focus:**

- Task create → `task_run` → persisted `run_events` / `tool_calls`.
- Knowledge ingest → embedding job → retrieval top-k (pgvector against test project or local Supabase).
- Eval run lifecycle: enqueue job → `eval_runs` status transitions.
- Supabase RLS: operator vs approver vs admin JWT fixtures.

**Environment:**

- Prefer **local Supabase CLI** for CI where possible; otherwise a dedicated **staging** project with isolated data.
- Never run integration tests against production.

---

## 4. Eval datasets (agent quality gate)

Eval is **not** a substitute for unit tests; it scores **versioned agent config** against golden scenarios aligned with the IT triage demo vertical ([PRODUCT_SPEC](PRODUCT_SPEC.md)).

**Artifacts (data model):**

- `eval_suites`, `eval_cases`, `eval_runs`, `eval_results`.

**Rules (product gates G3):**

- No `agent_version` may reach `ACTIVE` without a **passed** `eval_run` and an `approvals` row (admin break-glass only, audited).

**Dataset content:**

- Synthetic tickets covering classify → retrieve → tool choice → notify/escalate.
- Regression cases for known misclassifications fixed in prior versions.
- Negative cases: destructive tools blocked, low-confidence escalation.

**CI:**

- On PRs that change orchestrator prompts, routing, or tool policies: run **smoke eval** (subset).
- Before merge to `main` for evolution-related changes: run **full suite** on staging.

---

## 5. TestSprite MCP & E2E

TestSprite provides **browser-level** coverage of operator inbox, task detail, feedback, and approver promotion flows.

### 5.1 PRD (Product Requirements for TestSprite integration)

| ID | Requirement | Priority |
|----|-------------|----------|
| TS-1 | Run TestSprite against **staging** URL with test operator + approver accounts | P0 |
| TS-2 | Cover: login → task list → open task → submit feedback | P0 |
| TS-3 | Cover: approver queue → view eval summary → approve/reject (staging only) | P0 |
| TS-4 | Fail CI on P0 flow regression | P0 |
| TS-5 | Store run artifacts (screenshots, traces) linked from CI job summary | P1 |
| TS-6 | Nightly full suite on `main`; PR runs **smoke** subset | P1 |
| TS-7 | Document MCP invocation in repo (`docs/TESTING_STRATEGY.md` + agent contract I) | P1 |

### 5.2 MCP usage (agents & developers)

- Use the **TestSprite MCP** from Cursor for authoring and debugging flows during feature work.
- Check in **flow definitions / scenario IDs** (not API keys) under `tests/e2e/testsprite/` when the scaffold lands.
- Secrets: `TESTSPRITE_*` in CI only ([`.env.example`](../.env.example)).

### 5.3 When TestSprite runs in CI

| Trigger | TestSprite job |
|---------|----------------|
| PR touches `apps/web/**` | Smoke E2E (required check before human push approval) |
| PR touches shared auth/routing | Smoke E2E |
| Merge to `main` | Full E2E + nightly schedule |
| Release tag | Full E2E on production-like staging |

Per [README](../README.md) **push policy**: after initial remote bootstrap, **human approval** is required before push; CI must be green (unit + integration + applicable eval + TestSprite smoke).

---

## 6. Security tests

| Check | Tool / method | Frequency |
|-------|----------------|-----------|
| Secret leak prevention | gitleaks / GitHub secret scanning | Every push |
| Dependency audit | `npm audit`, `pip-audit` / Dependabot | Weekly + PR on lockfile change |
| RLS regression | Integration tests with role JWTs | Every PR |
| Tool policy default deny | Unit + integration | Every PR |
| OWASP API basics | ZAP baseline optional on staging | Pre-release |

Evolution and tool execution paths must include tests that **unapproved destructive tools never fire** without explicit policy + approval.

---

## 7. Local developer workflow

```text
# API (when scaffold exists)
pytest tests/unit
pytest tests/integration  # requires local Supabase

# Web
pnpm test

# Eval smoke (staging credentials)
# scripts/eval-smoke.sh

# TestSprite (MCP or CLI — staging URL)
# documented in tests/e2e/testsprite/README.md
```

---

## 8. CI pipeline (target state)

Phase 0 introduces GitHub Actions (or equivalent) with:

1. Lint + typecheck (web + api).
2. Unit tests.
3. Integration tests (Supabase service container or staging).
4. Eval smoke (conditional paths).
5. TestSprite smoke (conditional `apps/web`).
6. Security scanners (non-blocking → blocking as maturity increases).

**Branch protection:** `main` requires green required checks; no direct push without review after bootstrap.

---

## 9. Related documents

- [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) — agent handoff and when to run tests before commit.
- [ADR 0010](adr/0010-testsprite-and-eval-layers.md) — eval vs E2E separation.
- [PRODUCT_SPEC.md](PRODUCT_SPEC.md) — gates G1–G5 and demo vertical.
