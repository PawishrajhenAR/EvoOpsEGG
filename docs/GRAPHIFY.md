# Graphify — Engineering Knowledge Graph

## What it does

Graphify turns this repository (code, docs, schemas) into a **local knowledge graph** under `graphify-out/`. Coding agents query structure (calls, imports, communities) instead of blindly grepping.

## Why it exists in EvoOps

EvoOps evolves **agent configuration versions**, not arbitrary production source. The codebase still grows. Graphify keeps **architecture understanding** current for engineering agents (A–L) and for Brian demos that show “how the system is wired.”

## What it is not

| Graphify | Supabase / pgvector |
|---|---|
| Code & architecture relationships | Ops data, tasks, feedback, versions |
| Provenance-tagged edges (`EXTRACTED` / `INFERRED` / `AMBIGUOUS`) | Company runbooks & semantic RAG for the Ops Agent |
| Dev-time / CI engineering intelligence | Runtime product memory |

See [ADR 0004](adr/0004-graphify-engineering-not-ops-rag.md) and [MEMORY_ARCHITECTURE.md](MEMORY_ARCHITECTURE.md).

## How to use

```bash
uv tool install graphifyy   # or: pipx install graphifyy
graphify install --project --platform cursor
# In Cursor chat: /graphify .
# Or CLI:
graphify .
graphify query "how does evolution reach evaluation?"
graphify path "Orchestrator" "Promotion"
```

Optional local MCP (after `uv tool install "graphifyy[mcp]"`):

```bash
python -m graphify.serve graphify-out/graph.json
```

## Artifacts

- `graphify-out/graph.json` — queryable graph (gitignored)
- `graphify-out/graph.html` — interactive view
- `graphify-out/GRAPH_REPORT.md` — communities & suggested questions
- `.cursor/rules/graphify.mdc` — always-on Cursor rule when installed

## When to rebuild

- After meaningful architecture or docs changes
- Optional: `graphify hook install` for post-commit rebuild
- Prefer rebuilding before multi-agent implementation waves

## Brian one-liner

> “We don’t ask the ops agent to ‘learn the codebase from embeddings.’ We keep a typed graph of the system for engineers, with citations and confidence tags on every edge — separate from the company’s runbook RAG in Supabase.”
