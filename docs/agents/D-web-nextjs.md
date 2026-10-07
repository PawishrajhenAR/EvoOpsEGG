# Agent D — Web (Next.js)

**Pipeline step:** IMPLEMENT  
**Owns:** `apps/web/`

## Mission

Operator inbox, task detail, feedback, approver console, admin screens — Supabase Auth client-side with RLS.

## Responsibilities

- Tailwind UI aligned with PRODUCT_SPEC UX sections.
- Langfuse trace link-out from task detail.
- Env: `NEXT_PUBLIC_*` only on client.

## Out of scope

- API business logic duplication; call API for orchestration when required.

## Definition of done

- TestSprite-smokeable flows on staging (with I).
- Accessible forms for feedback (G4).

## Key references

ADR 0001; [TESTING_STRATEGY.md](../TESTING_STRATEGY.md) TestSprite PRD.
