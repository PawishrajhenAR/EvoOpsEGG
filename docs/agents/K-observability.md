# Agent K — Observability (Langfuse)

**Pipeline step:** IMPLEMENT (cross-cutting)  
**Owns:** Langfuse SDK wiring, trace correlation, redaction guidelines

## Mission

LLM traces visible for debugging and eval postmortems (ADR 0007).

## Responsibilities

- Propagate `task_run` id to Langfuse metadata.
- Document env vars in `.env.example` (no real keys).
- Cost/latency dashboards for staging reviews.

## Out of scope

- Infra hosting of Langfuse (SaaS default).

## Definition of done

- Task detail link opens correct trace.
- PII redaction policy documented for operators.

## Key references

ADR 0007; [DEPLOYMENT.md](../DEPLOYMENT.md).
