# EvoOps Development Workflow

**Status:** Planning baseline  
**Owner:** Principal Architect (A)

This workflow governs how human and **engineering agents** (A–L) change the EvoOps monorepo: read contracts first, implement in scope, test, document, commit, and hand off.

---

## 1. Agent execution pipeline

Each session follows this ordered pipeline. Do not skip steps without explicit human waiver.

```text
ARCHITECTURE → DATA_MODEL → IMPLEMENT → TEST → DOCS → COMMIT → NEXT AGENT
```

| Step | Primary agent | Outputs |
|------|---------------|---------|
| **ARCHITECTURE** | A — Principal Architect | ADRs, updates to `docs/ARCHITECTURE.md` (when it exists), boundary decisions |
| **DATA_MODEL** | B — Data & Supabase | Migrations, RLS policies, type alignment |
| **IMPLEMENT** | C–H (domain agents) | Code in owned paths (`apps/*`, `tests/*`) |
| **TEST** | I — Eval & Testing | Unit/integration/eval/TestSprite per [TESTING_STRATEGY](TESTING_STRATEGY.md) |
| **DOCS** | Session owner | Session log, status/roadmap deltas if instructed |
| **COMMIT** | Session owner | Conventional commit on feature branch |
| **NEXT AGENT** | A or human | Handoff note in session log + contract checklist |

**Architecture changes** require a new or updated **ADR** under `docs/adr/` before merge (see §4).

---

## 2. Branching strategy

| Branch prefix | Use |
|---------------|-----|
| `main` | Protected; demo-ready / release line |
| `feat/*` | User-facing or API features |
| `fix/*` | Bug fixes |
| `infra/*` | CI, deploy, Supabase infra, Docker |
| `test/*` | Test harness, eval fixtures, TestSprite flows |
| `refactor/*` | Behavior-preserving restructures |

**Flow:**

1. Branch from latest `main`.
2. Open PR when checks are green (or document blockers).
3. Squash or merge per team preference (default: merge commit for traceability until Phase 2).

**Push policy ([README](../README.md)):**

- **First push** to remote is authorized for bootstrap.
- **Later pushes** require explicit human approval after relevant tests pass.

Agents must **not** force-push `main` or push without human sign-off post-bootstrap.

---

## 3. Conventional commits

Format: `<type>(<scope>): <description>`

**Types:** `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `infra`, `eval`

**Scopes (examples):** `web`, `api`, `worker`, `supabase`, `evolution`, `orchestrator`, `ci`

**Examples:**

```text
feat(api): add task_run event streaming endpoint
fix(web): approver diff view for nested routing config
docs(adr): accept custom orchestrator decision
test(eval): add golden case for VPN ticket classification
infra(ci): run TestSprite smoke on web PRs
```

Breaking changes: `feat!:` or footer `BREAKING CHANGE:`.

---

## 4. Architecture Decision Records (ADRs)

- Location: `docs/adr/NNNN-short-title.md`
- Required when changing: stack, hosting, auth model, orchestration pattern, evolution boundaries, observability, or test gates.
- Template: Status, Context, Decision, Consequences (see existing ADRs).
- Link ADRs from `docs/ARCHITECTURE.md` when that file is maintained.

---

## 5. Code ownership (agents A–L)

| Agent | File | Owns |
|-------|------|------|
| A | [agents/A-principal-architect.md](agents/A-principal-architect.md) | ADRs, architecture, workflow |
| B | [agents/B-data-supabase.md](agents/B-data-supabase.md) | `supabase/migrations/` |
| C | [agents/C-api-fastapi.md](agents/C-api-fastapi.md) | `apps/api/` HTTP layer |
| D | [agents/D-web-nextjs.md](agents/D-web-nextjs.md) | `apps/web/` |
| E | [agents/E-orchestrator.md](agents/E-orchestrator.md) | Task runtime, routing |
| F | [agents/F-knowledge-rag.md](agents/F-knowledge-rag.md) | Ops RAG ingest/retrieve |
| G | [agents/G-tools-connectors.md](agents/G-tools-connectors.md) | Connectors, tool_calls |
| H | [agents/H-evolution-engine.md](agents/H-evolution-engine.md) | Proposals, version lifecycle |
| I | [agents/I-eval-testing.md](agents/I-eval-testing.md) | `tests/`, eval suites |
| J | [agents/J-security-authz.md](agents/J-security-authz.md) | RLS, tool policies, audit |
| K | [agents/K-observability.md](agents/K-observability.md) | Langfuse integration |
| L | [agents/L-devops-release.md](agents/L-devops-release.md) | CI/CD, [DEPLOYMENT](DEPLOYMENT.md) |

Agents must **not** edit `README.md` or `docs/PRODUCT_SPEC.md` unless the human explicitly assigns that scope.

---

## 6. Session protocol

Start/end checklists and log template: [SESSION_PROTOCOL.md](SESSION_PROTOCOL.md).

---

## 7. Definition of done (per PR)

- [ ] Scope matches assigned agent contract.
- [ ] Tests added/updated per [TESTING_STRATEGY](TESTING_STRATEGY.md).
- [ ] No secrets in diff; `.env.example` updated if new vars.
- [ ] ADR if architectural.
- [ ] Session log updated when work spans multiple sessions.
- [ ] Handoff note for **NEXT AGENT** when work is partial.

---

## 8. Related documents

- [SESSION_PROTOCOL.md](SESSION_PROTOCOL.md)
- [TESTING_STRATEGY.md](TESTING_STRATEGY.md)
- [DEPLOYMENT.md](DEPLOYMENT.md)
- [PRODUCT_SPEC.md](PRODUCT_SPEC.md) (read-only for agents unless directed)
