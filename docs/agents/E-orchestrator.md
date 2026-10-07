# Agent E — Orchestrator

**Pipeline step:** IMPLEMENT  
**Owns:** Task runtime inside `apps/api` (orchestrator package)

## Mission

Execute classify → retrieve → route → act loop per ADR 0006 using **active** `agent_version` config.

## Responsibilities

- Persist `run_events`, `tool_calls`; snapshot version id on `task_run`.
- Invoke F (retrieval) and G (tools) through stable interfaces.
- Langfuse spans (with K).

## Out of scope

- Evolution proposal authoring (H); eval scoring (I).

## Definition of done

- Demo vertical runs end-to-end on staging.
- Low-confidence escalation path tested.

## Key references

ADR 0006, 0005, 0007.
