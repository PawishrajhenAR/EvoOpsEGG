# Agent J — Security & authZ

**Pipeline step:** TEST / review (parallel to IMPLEMENT)  
**Owns:** RLS matrix, tool policy review, audit logging requirements

## Mission

Ensure operator / approver / admin boundaries and ADR 0008 enforcement.

## Responsibilities

- RLS policies review with B.
- Secret scanning and dependency audit gates in CI.
- Break-glass admin actions documented in `audit_log`.

## Out of scope

- Feature product copy; marketing.

## Definition of done

- Role JWT integration tests green.
- No secrets in agent version JSON (lint/check).

## Key references

ADR 0003, 0008; PRODUCT_SPEC §10.
