# Agent H — Evolution engine

**Pipeline step:** IMPLEMENT  
**Owns:** Signals/patterns → proposals → draft `agent_versions`

## Mission

Propose **config-only** mutations (ADR 0005); never edit app source.

## Responsibilities

- `evolution_proposals` rationale and diffs.
- State transitions toward `EVALUATING` / `PENDING_APPROVAL`.
- Block auto-activation without eval + approver.

## Out of scope

- Eval suite definition (I); approver UI (D).

## Definition of done

- Brian narrative: proposed → tested → improved with audit trail.
- Rollback story uses prior `ACTIVE` version (G5).

## Key references

ADR 0005, 0010; PRODUCT_SPEC §6.5–6.7.
