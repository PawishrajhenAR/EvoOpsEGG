# ADR 0010: TestSprite and eval layers

**Status:** Accepted  
**Date:** 2026-10-07

## Context

EvoOps quality depends on (1) **code** correctness and (2) **agent config** quality. UI regressions are poorly caught by unit tests alone; config regressions require golden scenarios.

## Decision

Separate two layers:

| Layer | Tooling | Validates |
|-------|---------|-----------|
| **Eval** | `eval_suites` / `eval_cases` / jobs in API | Draft `agent_versions` behavior vs golden tasks |
| **E2E** | **TestSprite** (MCP + CI) | Web flows: inbox, feedback, approver promotion |

**Gates:**

- Eval pass required before `PENDING_APPROVAL` → `ACTIVE`.
- TestSprite smoke on PRs touching `apps/web`; full suite on `main`/nightly/release.

TestSprite targets **staging** (or labeled preview). Eval runs against staging API + DB fixtures.

## Consequences

- **Positive:** Clear ownership — agent I for eval/tests, TestSprite for UX paths.
- **Negative:** CI time and staging upkeep; two systems to maintain.
- **Follow-ups:** `docs/TESTING_STRATEGY.md` PRD for TestSprite; Phase 0+ CI wiring by L.
