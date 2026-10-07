# EvoOps

**Self-Evolving AI Operations Platform**

EvoOps helps internal IT and operations teams triage work automatically: classify incoming tickets, retrieve the right runbook, choose and invoke tools, act or notify stakeholders, capture human feedback, and **evolve agent configuration** (prompts, routing, tool policies)—never arbitrary production source code—through evaluation, approval, and controlled rollout.

Phase 0 scaffold is underway: Next.js (`apps/web`) and FastAPI (`apps/api`) health shells run locally. Full product features start in later phases. See [Local setup](docs/LOCAL_SETUP.md), [Project Status](docs/PROJECT_STATUS.md), and [Roadmap](docs/ROADMAP.md).

**GitHub:** [https://github.com/PawishrajhenAR/EvoOpsEGG.git](https://github.com/PawishrajhenAR/EvoOpsEGG.git)

---

## Product summary

| Aspect | Choice |
|--------|--------|
| **Name** | EvoOps — Self-Evolving AI Operations Platform |
| **Demo vertical** | IT / internal ops triage |
| **Tenancy** | Single organization |
| **Roles** | `operator`, `approver`, `admin` |
| **Evolution scope** | Mutates **agent version config** only (prompts, routing, tool policies) |
| **Push policy** | First push to remote is authorized; later pushes require human approval after testing |

### Demo flow (what we build toward)

1. **Classify** — An incoming ticket or alert is parsed and categorized (severity, queue, intent).
2. **Retrieve** — Relevant runbooks and knowledge chunks are fetched (pgvector RAG over ops knowledge).
3. **Choose tool** — Routing and tool policies decide which connector/action to use (or escalate).
4. **Act / notify** — Execute approved tools (e.g. status update, Slack/email via Resend) or queue for human.
5. **Human feedback** — Operators rate outcomes, correct labels, or flag unsafe behavior.
6. **Evolution** — Signals and patterns propose changes to the **next draft agent version**.
7. **Eval** — Automated suites score draft versions against golden tasks and regression cases.
8. **Approve** — Approvers promote `PENDING_APPROVAL` → `ACTIVE` after review.
9. **Improve** — The new active version replaces the prior one; rollbacks remain one click away.

**Graphify** is used for **engineering intelligence** (code/repo context for builders)—not as the ops ticket RAG backend.

---

## Brian-demo narrative (observed → improved)

Use this story when explaining EvoOps to stakeholders (e.g. “Brian” demo):

| Stage | What happens | What EvoOps records |
|-------|----------------|---------------------|
| **Observed** | Tickets pile up; operators repeat the same triage steps; wrong runbooks get attached sometimes. | `tasks`, `task_runs`, `run_events`, `tool_calls`, Langfuse traces |
| **Learned** | Feedback and outcomes show which classifications and tool choices worked. | `feedback`, `signals`, `patterns` |
| **Proposed** | The platform drafts a new **agent version** with updated prompts/routing/tool policy—not a code deploy. | `evolution_proposals`, `agent_versions` (`DRAFT`) |
| **Tested** | Eval jobs run against fixed scenarios; failures block promotion. | `eval_suites`, `eval_runs`, `eval_results`, status `EVALUATING` / `FAILED_EVALUATION` |
| **Improved** | Approver activates the version; operators see better triage on the next tickets. | `approvals`, `agent_versions` (`ACTIVE`), `audit_log` |

The loop closes when **active version config** changes while **application source** stays stable and reviewable.

---

## Stack

| Layer | Technology | Hosting |
|-------|------------|---------|
| Web UI | Next.js, TypeScript, Tailwind | Vercel |
| API & workers | FastAPI (Python) | Railway or Render |
| Data & auth | Supabase (Postgres, Auth, RLS, pgvector) | Supabase |
| LLM | OpenAI | API |
| Email | Resend | API |
| Observability | Langfuse | Cloud / self-host |
| Engineering intel | Graphify | Separate from ops RAG |
| E2E | TestSprite | CI / scheduled |

---

## Repository layout (planned)

```
EvoOpsEGG/
├── apps/
│   ├── web/          # Next.js operator & approver UI
│   └── api/          # FastAPI: tasks, agents, evolution, jobs
├── supabase/
│   └── migrations/   # Schema, RLS, vector indexes
├── scripts/          # Dev and deploy helpers
├── tests/
│   └── unit/         # API and domain unit tests
└── docs/             # Product, architecture, data model, status, roadmap
```

Empty placeholders exist today; implementation begins in Phase 0.

---

## How to read the docs

Read in this order for a full picture:

1. **[Product Spec](docs/PRODUCT_SPEC.md)** — Goals, personas, demo vertical, functional requirements, non-goals.
2. **[Architecture](docs/ARCHITECTURE.md)** — Components, sync vs async paths, deployment map, integration boundaries.
3. **[Data Model](docs/DATA_MODEL.md)** — Tables, relationships, agent version state machine, audit and jobs.
4. **[Project Status](docs/PROJECT_STATUS.md)** — What is done now (planning) and what is blocked on Phase 0.
5. **[Roadmap](docs/ROADMAP.md)** — Phases 0–14 from scaffold through demo-ready evolution loop.

For day-to-day execution, keep **PROJECT_STATUS** and **ROADMAP** open; treat **DATA_MODEL** and **ARCHITECTURE** as contracts when implementing migrations and API shapes.

---

## Contributing & remote policy

- **First push** to [EvoOpsEGG](https://github.com/PawishrajhenAR/EvoOpsEGG.git) is authorized to establish the remote and baseline docs/scaffold.
- **Subsequent pushes** require explicit human approval after relevant tests (unit, eval where applicable, TestSprite E2E for user-facing changes).

Do not commit secrets. Use Supabase and Vercel/Railway/Render environment configuration for keys (OpenAI, Resend, Langfuse, etc.).

---

## License

TBD — set before public release.
