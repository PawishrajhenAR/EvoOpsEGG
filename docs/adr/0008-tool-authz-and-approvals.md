# ADR 0008: Tool authorization and approvals

**Status:** Accepted  
**Date:** 2026-10-07

## Context

Agents that invoke external systems (email, Slack, ticket updates) create security and abuse risk. Evolution must not widen tool access without review.

## Decision

- **`tool_policies`** default **deny**; allowlists per connector action with optional rate limits.
- Destructive or high-impact tools require **explicit policy** and may require **human approval** before execution (configurable per tool).
- All invocations logged in **`tool_calls`**; denials logged in **`audit_log`**.
- Version promotion requires approver role; tool policy changes are admin-scoped and audited.
- Secrets live in env/vault references on **`connectors`**, never in `agent_versions` JSON.

RLS ensures operators cannot approve their own version promotions.

## Consequences

- **Positive:** Defense in depth for demo and production single-org use.
- **Negative:** More configuration upfront for each connector.
- **Follow-ups:** Security tests in TESTING_STRATEGY; agent J owns matrix tests.
