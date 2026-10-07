# ADR 0007: Langfuse for LLM observability

**Status:** Accepted  
**Date:** 2026-10-07

## Context

Operators and developers need to debug misclassification, latency spikes, and cost. Task timelines in the UI are insufficient for token-level inspection.

## Decision

Use **Langfuse** as the primary **LLM observability** platform:

- API/worker SDK wraps OpenAI calls with traces/spans.
- Correlate Langfuse trace id with `task_run` id (stored on run or events).
- UI provides link-out from task detail for operator/debug roles.

Metrics: latency, cost, model version — reviewed during eval failures and evolution proposals.

## Consequences

- **Positive:** Industry-standard tracing; supports demo narrative “observed → learned.”
- **Negative:** Additional secrets and data residency considerations; PII must not land in prompts logged against policy.
- **Follow-ups:** Agent K documents env vars and redaction rules.
