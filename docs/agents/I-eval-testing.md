# Agent I — Eval & testing

**Pipeline step:** TEST  
**Owns:** `tests/`, eval suite fixtures, TestSprite scenario catalog

## Mission

Implement [TESTING_STRATEGY.md](../TESTING_STRATEGY.md): unit, integration, eval datasets, TestSprite E2E, security test hooks.

## Responsibilities

- `eval_suites` / `eval_cases` content for demo vertical.
- CI path filters and conditional jobs (with L).
- TestSprite MCP flows for P0 PRD (TS-1–TS-4).

## Out of scope

- Production deploy (L); schema without B coordination.

## Definition of done

- G3 enforced by automated eval gate in CI/staging.
- PR checklist tests documented in session log.

## Key references

ADR 0010; [TESTING_STRATEGY.md](../TESTING_STRATEGY.md).
