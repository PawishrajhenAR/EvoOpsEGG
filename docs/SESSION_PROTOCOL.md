# EvoOps Session Protocol

**Status:** Planning baseline  
**Owner:** Principal Architect (A)

Every Cursor/agent session that touches the EvoOps repo should **start** and **end** with this protocol so humans and agents share context across handoffs.

---

## 1. Session start checklist

- [ ] Read [PROJECT_STATUS.md](PROJECT_STATUS.md) and [ROADMAP.md](ROADMAP.md) (when present).
- [ ] Read assigned **agent contract** under `docs/agents/`.
- [ ] Confirm branch: create `feat/*`, `fix/*`, etc. from `main` if implementing.
- [ ] Load architecture contracts: [ARCHITECTURE.md](ARCHITECTURE.md), [DATA_MODEL.md](DATA_MODEL.md) (when present).
- [ ] Note **push policy**: post-bootstrap pushes need human approval after tests ([README](../README.md)).
- [ ] Identify **NEXT** pipeline step: ARCHITECTURE → … → COMMIT → NEXT AGENT ([DEVELOPMENT_WORKFLOW](DEVELOPMENT_WORKFLOW.md)).
- [ ] Create or append session log under `docs/sessions/` (see §3).

---

## 2. Session end checklist

- [ ] Run tests appropriate to scope ([TESTING_STRATEGY](TESTING_STRATEGY.md)).
- [ ] Update session log: outcomes, blockers, files touched, **NEXT AGENT** recommendation.
- [ ] Commit with conventional message if human requested commit or session policy allows.
- [ ] Do **not** push without human approval (except authorized bootstrap).
- [ ] Flag ADR need if decision was architectural but ADR not yet written.
- [ ] Leave working tree clean or document WIP in session log.

---

## 3. Session log template

Create `docs/sessions/NNN-short-slug.md` (zero-padded sequence):

```markdown
# Session NNN — <title>

| Field | Value |
|-------|--------|
| **Date** | YYYY-MM-DD |
| **Agent role** | e.g. Principal Architect (A) |
| **Branch** | feat/... or n/a |
| **Push** | none / human-approved / bootstrap |

## Goal

What this session intended to deliver.

## Work completed

- Bullet list of concrete outcomes.

## Files touched

- `path/to/file` — brief note

## Tests

- What ran and result (or "not run — reason").

## Blockers / risks

- …

## Handoff — NEXT AGENT

**Recommended:** <agent letter + name>  
**Pipeline step:** IMPLEMENT | TEST | …  
**Notes:** …
```

---

## 4. Session numbering

- **000** — Planning complete ([sessions/000-planning.md](sessions/000-planning.md)).
- Increment for each substantial session (`001-scaffold-monorepo`, etc.).

---

## 5. Related documents

- [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md)
- [docs/agents/](agents/) — role contracts
