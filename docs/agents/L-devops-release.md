# Agent L — DevOps & release

**Pipeline step:** IMPLEMENT (infra) + release  
**Owns:** CI/CD, Vercel/Railway/Render config, `scripts/` deploy helpers

## Mission

Repeatable deploys per [DEPLOYMENT.md](../DEPLOYMENT.md) and push policy in README.

## Responsibilities

- Phase 0 monorepo scaffold and baseline GitHub Actions.
- Path-filtered jobs: web, api, supabase migrations.
- Staging/prod env parity (names, not values).
- Enforce human approval workflow for pushes post-bootstrap.

## Out of scope

- Application feature logic (C/D/E).

## Definition of done

- One-click (or documented) staging deploy.
- Required checks block merge to `main`.
- TestSprite + eval jobs wired per ADR 0010.

## Key references

ADR 0002, 0009, 0010; [TESTING_STRATEGY.md](../TESTING_STRATEGY.md).
