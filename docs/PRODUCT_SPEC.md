# EvoOps — Product Specification

**Version:** 0.1 (planning)  
**Status:** Approved for implementation planning; code Phase 0 not started  
**Product name:** EvoOps — Self-Evolving AI Operations Platform

---

## 1. Vision

Operations teams spend too much time on repetitive triage: reading tickets, guessing intent, hunting runbooks, and clicking through the same tools. EvoOps automates that loop with an **agent** whose behavior is defined by **versioned configuration** (prompts, routing rules, tool policies). When reality diverges from expectations, the platform **learns from feedback and signals**, proposes config mutations, **evaluates** them offline, and requires **human approval** before a new version goes **active**.

Evolution **never** auto-edits arbitrary application source in production. It only mutates stored agent version config under governance.

---

## 2. Problem statement

| Pain | Current state | EvoOps outcome |
|------|---------------|----------------|
| Slow first response | Manual classification | Consistent auto-classification with confidence and escalation |
| Wrong playbook | Search is keyword-heavy | RAG over curated ops knowledge (`knowledge_documents` / `knowledge_chunks`) |
| Tool sprawl | Tribal knowledge of which API to hit | Declarative `tool_policies` + audited `tool_calls` |
| No improvement loop | Post-mortems are separate | Feedback → signals → evolution proposals → eval → approval |
| Unsafe “self-modifying AI” fear | Ad-hoc prompt edits in chat | Draft versions, eval gates, approver role, full `audit_log` |

---

## 3. Demo vertical: IT / internal ops triage

The reference scenario for v1 demos and eval suites:

1. **Ingress** — Ticket arrives (simulated webhook, email parse, or manual create in UI) as a `task`.
2. **Classify** — Agent assigns category, priority, and suggested queue; low confidence → human queue.
3. **Retrieve runbook** — Top-k chunks from internal runbooks (not Graphify; Graphify is for engineering intel only).
4. **Choose tool** — Examples: update ticket status, fetch asset record, send notification (Resend), post to Slack (connector).
5. **Act or notify** — Execute allowed tools per policy; record every step in `run_events` and `tool_calls`.
6. **Human feedback** — Operator confirms, corrects, or rejects outcome (`feedback` types).
7. **Evolution** — System aggregates `signals` / `patterns`, creates `evolution_proposals` linked to new `agent_versions` (DRAFT).
8. **Eval** — `eval_runs` score draft vs golden tasks; pass → `PENDING_APPROVAL`.
9. **Approve** — Approver promotes to `ACTIVE`; previous active version may be `ROLLED_BACK` if needed.

---

## 4. Personas & roles (single org)

| Role | Persona | Capabilities |
|------|---------|--------------|
| **operator** | L1/L2 ops, on-call | Run tasks, view traces, submit feedback, cannot approve versions |
| **approver** | Team lead, change manager | All operator capabilities + approve/reject agent versions, view eval results |
| **admin** | Platform owner | User/role management, connectors, tool policies, knowledge ingestion, org settings |

Authentication and authorization are enforced via **Supabase Auth** and **RLS** on all tenant data. There is no multi-org switcher in v1.

---

## 5. Goals (measurable)

- **G1** — End-to-end triage demo completes in under 2 minutes wall-clock for a synthetic ticket (excluding human approval wait).
- **G2** — 100% of tool invocations and version promotions appear in `audit_log`.
- **G3** — No agent version reaches `ACTIVE` without `eval_runs` status passed and an `approvals` row (except admin break-glass documented in audit).
- **G4** — Operators can submit feedback on ≥95% of terminal task states from the UI.
- **G5** — Rollback from new `ACTIVE` to prior version in one action, status `ROLLED_BACK` on superseded version.

---

## 6. Functional requirements

### 6.1 Agent lifecycle

- Define logical agents in `agent_definitions` (stable key, description).
- Maintain immutable-ish history in `agent_versions` with JSON config: system prompts, classifier rubric, retrieval params, routing graph, tool policy refs.
- State machine: `DRAFT` → `EVALUATING` → `PASSED` → `PENDING_APPROVAL` → `APPROVED` → `ACTIVE`, with terminal/alternate states `FAILED_EVALUATION`, `REJECTED`, `ROLLED_BACK`.
- Exactly one `ACTIVE` version per agent definition at a time (enforced in API + DB constraint).

### 6.2 Task execution

- Create `tasks` from UI or connector webhooks.
- Each execution is a `task_run` linked to the **active** agent version at start time (snapshot id stored).
- Stream or poll `run_events` for UX; persist LLM and tool steps for Langfuse correlation.

### 6.3 Knowledge (ops RAG)

- Ingest `knowledge_documents` (runbooks, policies); chunk into `knowledge_chunks` with embeddings in pgvector.
- Retrieval scoped by document tags and RLS; no cross-org leakage (single org still uses RLS for role-based doc visibility if needed).

### 6.4 Tools & connectors

- `connectors` store credentials references (vault/env), not plaintext secrets in DB.
- `tool_policies` define allowlists, rate limits, and required approval for destructive tools.
- All executions logged in `tool_calls`.

### 6.5 Feedback & learning

- Structured `feedback` (thumbs, correction labels, free text).
- Derived `signals` (automated metrics from runs) and `patterns` (aggregated trends) feed evolution.

### 6.6 Evolution & eval

- `evolution_proposals` describe intended config diffs and rationale.
- Applying a proposal creates or updates a DRAFT `agent_version`.
- `eval_suites` and `eval_cases` define golden behavior; `eval_runs` / `eval_results` gate promotion.

### 6.7 Approvals & audit

- `approvals` record approver identity, decision, comment, version id.
- `audit_log` append-only record for security-relevant actions.

### 6.8 Background work

- `jobs` table for async workers: embedding backfill, eval batches, notification retries.

---

## 7. Non-goals (v1)

- Multi-tenant SaaS with org billing and self-signup.
- Autonomous modification of Next.js/FastAPI source or deployment configs.
- Using Graphify as the ops ticket knowledge base (Graphify is engineering intelligence only).
- Full ITSM replacement (ServiceNow/Jira parity).
- Unsupervised auto-activation of agent versions without eval + approver (except documented admin break-glass).

---

## 8. User experience (high level)

### Operator dashboard

- Task inbox, filters by status and classification.
- Task detail: timeline of `run_events`, retrieved chunks, tool results, feedback form.
- Link-out to Langfuse trace for debugging.

### Approver console

- Queue of versions in `PENDING_APPROVAL`.
- Side-by-side diff of config vs current `ACTIVE`.
- Eval summary and failure drill-down.

### Admin console

- Connectors, tool policies, knowledge upload, user role assignment, eval suite management.

---

## 9. Integrations

| Integration | Purpose |
|-------------|---------|
| OpenAI | Classification, summarization, proposal drafting, embedding |
| Resend | Operator/customer email notifications |
| Langfuse | Trace LLM calls, cost and latency dashboards |
| Graphify | Repo/engineering context for **developers** building EvoOps, not runtime ops RAG |
| TestSprite | E2E coverage of critical UI flows |

---

## 10. Security & compliance posture

- RLS on all application tables; service role only on backend workers with minimal scope.
- Secrets in environment / Supabase vault patterns—never in agent version config JSON.
- Tool policies default **deny**; explicit allow per connector action.
- Evolution proposals and version diffs are readable by approvers before promotion.
- Push policy: after initial remote bootstrap, production-impacting changes require human sign-off and test passage.

---

## 11. Success criteria for “demo ready”

- Live demo of the nine-step vertical on staging with at least one eval suite green.
- One recorded rollback scenario.
- Brian narrative (observed → learned → proposed → tested → improved) walkthrough under 10 minutes.

See [ROADMAP.md](ROADMAP.md) for phase mapping and [PROJECT_STATUS.md](PROJECT_STATUS.md) for current completion.
