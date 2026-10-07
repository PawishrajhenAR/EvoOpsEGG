# Agent G — Tools & connectors

**Pipeline step:** IMPLEMENT  
**Owns:** Connector adapters, tool execution, Resend/Slack/etc.

## Mission

Execute allowed tools per `tool_policies`; log everything; default deny (ADR 0008).

## Responsibilities

- `connectors` credential refs (env/vault).
- Rate limits and approval gates for destructive actions.
- Structured results for `tool_calls` table.

## Out of scope

- UI for connector CRUD (D admin screens consume API).

## Definition of done

- Deny-by-default tests pass (J/I).
- Demo tools: notify via Resend at minimum.

## Key references

ADR 0008; PRODUCT_SPEC §6.4.
