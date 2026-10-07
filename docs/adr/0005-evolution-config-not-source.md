# ADR 0005: Evolution mutates config, not application source

**Status:** Accepted  
**Date:** 2026-10-07

## Context

Self-evolving systems raise safety concerns if they rewrite deployed code or infrastructure. EvoOps product promise is controlled improvement of **agent behavior** via versioned configuration.

## Decision

The evolution loop may create and update **`agent_versions` JSON config** only: prompts, classifier rubrics, retrieval parameters, routing graphs, tool policy references.

Evolution **must not**:

- Auto-edit Next.js, FastAPI, or migration source in production.
- Auto-change Vercel/Railway/Render deployment settings.
- Activate a new version without eval pass + approver (except documented admin break-glass in `audit_log`).

Proposals are recorded in `evolution_proposals` with human-readable rationale and diffs for approvers.

## Consequences

- **Positive:** Aligns with G3; reduces fear of uncontrolled self-modification.
- **Negative:** Some improvements still require normal engineering PRs for code changes.
- **Follow-ups:** Agent H owns proposal → draft version pipeline; eval gate ADR 0010.
