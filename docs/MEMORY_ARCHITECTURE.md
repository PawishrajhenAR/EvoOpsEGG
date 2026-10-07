# EvoOps Memory Architecture

EvoOps memory is split into **operational memory** (Postgres + pgvector, queried during ticket triage and evolution) and **code knowledge** (Graphify artifacts under `graphify-out/`, engineering-only). Runtime agents never treat Graphify output as ticket RAG.

**Single org** deployment; all memory tables use RLS for role separation (`operator`, `approver`, `admin`).

---

## Memory types overview

| Type | Purpose | Store | Primary readers | Primary writers |
|------|---------|-------|-----------------|-----------------|
| **Episodic** | What happened on specific runs | Postgres | Retriever (context), Signal Extractor | Orchestrator, Ingest Worker |
| **Semantic** | Stable ops knowledge (runbooks, policies) | Postgres + pgvector | Retriever | Admin ingest jobs, feedback-driven re-rank |
| **Feedback** | Human judgments on outcomes | Postgres | Signal Extractor, Retriever boost | Feedback Normalizer |
| **Procedural** | How-to sequences, checklists tied to playbooks | Postgres | Planner/Router, Retriever | Admin, Evolution (config-linked ids only) |
| **Code knowledge** | Repo structure, symbols, eng docs | Graphify `graphify-out/` | Engineering agents A–L | Graphify indexer |

```mermaid
flowchart LR
  subgraph ops_mem["Operational memory — Postgres"]
    EP[Episodic]
    SE[Semantic + vectors]
    FB[Feedback]
    PR[Procedural]
  end

  subgraph code_mem["Code knowledge — Graphify"]
    GF[graphify-out/]
  end

  RET[Retriever] --> EP
  RET --> SE
  RET --> FB
  RET --> PR
  PL[Planner/Router] --> PR
  SE -.->|embed| VEC[(pgvector)]

  EA[Eng agents A–L] --> GF
  GF -.x|not in triage path| RET
```

---

## Boundary rules (hard)

1. **Retriever** query sources are limited to `episodic_memory`, `semantic_chunks`, aggregated `feedback`, and `procedural_memory`—never filesystem Graphify paths.
2. **Evolution Proposer** may reference pattern exemplar `task_run_id`s and config knobs; it must not embed raw code files from Graphify into promoted config.
3. **Ops Agent** context windows include only citations returned by Retriever (chunk ids + hashed content), not whole tables.
4. **Graphify** outputs are versioned in git or CI artifacts; production API pods do not mount `graphify-out/` unless running an explicit engineering job.

---

## Episodic memory

### Intent

Capture run-scoped facts for “what we already tried on this ticket” and short-term org narrative (recent incidents).

### Schema (conceptual)

**Table:** `episodic_memory`

| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid | PK |
| `task_id` | uuid | FK |
| `task_run_id` | uuid | FK, nullable for ingest-only notes |
| `kind` | enum | `ticket_summary`, `tool_result_digest`, `operator_note`, `system_event` |
| `content` | text | Redacted narrative |
| `structured` | jsonb | Machine fields (status codes, external ids) |
| `embedding` | vector(1536) | Optional; for “similar past runs” |
| `created_at` | timestamptz | |
| `expires_at` | timestamptz | TTL for demo noise control |

### Write paths

| Writer | When |
|--------|------|
| Ingest Worker | Initial `ticket_summary` from normalized payload |
| Orchestrator | Step summaries after terminal status |
| Invoke Service | `tool_result_digest` (truncated, no secrets) |

### Read paths

Retriever includes episodic hits when `task_id` matches or embedding similarity &gt; threshold with **time decay** (default 30 days).

---

## Semantic memory (RAG)

### Intent

Runbooks, policy excerpts, asset hints, FAQ—curated chunks with metadata.

**Table:** `semantic_chunks`

| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid | PK |
| `source_uri` | text | Internal doc id, not arbitrary URL |
| `title` | text | |
| `content` | text | Chunk body |
| `metadata` | jsonb | `queue`, `severity`, `product`, `version` |
| `embedding` | vector(1536) | OpenAI embedding model configurable |
| `is_active` | boolean | Soft delete |
| `updated_at` | timestamptz | |

### Ingestion pipeline

1. Admin uploads markdown/HTML or syncs from git-backed `docs/ops/**`.
2. Chunker (deterministic): heading-aware splits, max 800 tokens, 100 token overlap.
3. Embed job writes vectors batch-wise.
4. **No LLM chunking in MVP**—optional later for table-heavy docs.

### Retrieval algorithm (Retriever)

Hybrid score:

```
score = w_vec * cosine_sim(query_emb, chunk_emb)
      + w_kw  * ts_rank(tsv, query)
      + w_fb  * feedback_boost(chunk_id)
      + w_rec * recency_boost(updated_at)
```

Defaults in `agent_version_config.retrieval`: `w_vec=0.55`, `w_kw=0.25`, `w_fb=0.10`, `w_rec=0.10`, `top_k=8`, `min_score=0.72`.

Post-filter: metadata must match routing decision queue/severity when fields present.

---

## Feedback memory

### Intent

Human labels drive signals and retrieval boosts—not direct prompt mutation without evolution pipeline.

**Table:** `feedback`

| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid | |
| `task_run_id` | uuid | |
| `operator_id` | uuid | Supabase auth user |
| `rating` | smallint | -1, 0, 1 |
| `labels` | text[] | e.g. `wrong_queue`, `good_tool_choice` |
| `correction` | jsonb | Optional corrected classification |
| `comment` | text | Sanitized length cap |
| `created_at` | timestamptz | |

**Feedback Normalizer** validates enums, strips HTML, maps UI payloads to this shape.

### Aggregates for learning

Materialized view or scheduled rollup: `feedback_chunk_stats(chunk_id)` → boost factor clamped [0.8, 1.2].

---

## Procedural memory

### Intent

Playbooks as ordered steps (checklists), linked from routing config—not freeform LLM memory.

**Table:** `procedural_memory`

| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid | |
| `playbook_id` | text | Stable key referenced in routing config |
| `step_order` | int | |
| `instruction` | text | Operator-facing |
| `required_tool_action_id` | text | Optional manifest action |
| `metadata` | jsonb | |

Planner/Router selects `playbook_id`; Retriever pulls procedural rows for Ops Agent checklist context.

Evolution may switch `playbook_id` or step text **only** via new agent version config pointing at existing playbook ids or admin-approved procedural rows—not ad-hoc strings from LLM.

---

## pgvector operations

| Concern | Choice |
|---------|--------|
| Index | HNSW on `semantic_chunks.embedding`, optional on episodic |
| Dimension | 1536 (text-embedding-3-small default) |
| Distance | Cosine (`vector_cosine_ops`) |
| Refresh | Re-embed on content change; background job |

Query pattern (Retriever):

```sql
SELECT id, title, content,
       1 - (embedding <=> :query_emb) AS vec_sim
FROM semantic_chunks
WHERE is_active = true
ORDER BY embedding <=> :query_emb
LIMIT :k;
```

Combine with keyword leg using `content_tsv` generated column.

---

## Graphify code knowledge (engineering boundary)

### Location

```
graphify-out/
  manifest.json
  graph.db | graph.json
  summaries/
```

### Consumers

| Consumer | Usage |
|----------|-------|
| Agent A (Repo Cartographer) | Service map |
| Agent C (API Contract Smith) | Route discovery |
| Agent G/H | Prompt/policy context during **dev** |
| Cursor MCP (optional) | Code search in engineering sessions |

### Prohibited

- Mounting Graphify DB as Retriever source in production triage.
- Automatic promotion of Graphify text into `semantic_chunks` without human admin ingest review.

Sync path if needed: human exports vetted summary markdown from Graphify → admin semantic ingest job.

---

## Memory ↔ agent version config

Active version may tune:

| Key | Affects |
|-----|---------|
| `retrieval.top_k`, `min_score`, weights | Retriever only |
| `routing.playbook_id` | Procedural selection |
| `prompts.*` | Ops Agent phrasing—not memory contents |

Evolution Proposer **cannot** write arbitrary rows into semantic/episodic tables; content changes go through admin ingest or feedback aggregates.

---

## Retention & privacy

| Data | Retention (demo defaults) |
|------|---------------------------|
| Episodic | 90 days |
| Semantic | Until deactivated |
| Feedback | Indefinite (aggregated) |
| Tool result digests | Redact PII patterns; store hashes of raw upstream payload refs |

Operators may request deletion of `comment` fields; episodic structured external ids remain for audit.

---

## Consistency & caching

| Layer | Strategy |
|-------|----------|
| Retriever | Read replica ok; stale up to 60s for semantic |
| Embeddings | Strong consistency after ingest job marks `is_active` |
| Config | Promotion Service busts Retriever cache key `(agent_version_id)` |

---

## Failure modes

| Failure | Behavior |
|---------|----------|
| Vector index missing | Retriever keyword-only fallback; log warning |
| Empty semantic corpus | Ops Agent escalates with `missing_knowledge` label |
| Embedding API down | Queue embed jobs; retrieval degraded mode |
| Feedback spam | Rate limit per operator; outlier detection in Signal Extractor |

---

## Related documents

- [Agent Architecture](AGENT_ARCHITECTURE.md) — Retriever, Feedback Normalizer
- [Evolution Engine](EVOLUTION_ENGINE.md) — patterns from feedback/signals
- [Security Architecture](SECURITY_ARCHITECTURE.md) — RLS on memory tables
