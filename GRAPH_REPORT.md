# Graph Report - apps\api  (2026-10-07)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 101 nodes · 180 edges · 8 communities (7 shown, 1 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 18 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]

## God Nodes (most connected - your core abstractions)
1. `ToolRegistry` - 12 edges
2. `PolicyGuard` - 10 edges
3. `Retriever` - 9 edges
4. `OpsAgent` - 9 edges
5. `TaskRequest` - 9 edges
6. `AgentVersionConfig` - 8 edges
7. `RouteDecision` - 8 edges
8. `ToolCall` - 8 edges
9. `VersionStatus` - 7 edges
10. `AgentAnswer` - 7 edges

## Surprising Connections (you probably didn't know these)
- `AgentVersionConfig` --uses--> `PolicyGuard`  [INFERRED]
  evoops/ops_agent.py → evoops/security/policy.py
- `AgentAnswer` --uses--> `PolicyGuard`  [INFERRED]
  evoops/ops_agent.py → evoops/security/policy.py
- `OpsAgent` --uses--> `PolicyGuard`  [INFERRED]
  evoops/ops_agent.py → evoops/security/policy.py
- `AgentAnswer` --uses--> `Retriever`  [INFERRED]
  evoops/ops_agent.py → evoops/knowledge/retriever.py
- `AgentVersionConfig` --uses--> `Retriever`  [INFERRED]
  evoops/ops_agent.py → evoops/knowledge/retriever.py

## Import Cycles
- None detected.

## Communities (8 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.15
Nodes (17): Any, Hybrid search over runbooks and FAQs for the Ops Agent., Retriever, AgentAnswer, AgentVersionConfig, OpsAgent, Ops Agent — LLM-driven IT triage actor bound to an agent_version config., Reproducible behaviour — the only thing evolution mutates. (+9 more)

### Community 1 - "Community 1"
Cohesion: 0.14
Nodes (15): CandidateVersion, EvolutionEngine, EvolutionProposer, Pattern, PatternDetector, PromotionService, Evolution engine — pattern → candidate config → eval → promote., Deterministic mapping of feedback and errors → signals. (+7 more)

### Community 2 - "Community 2"
Cohesion: 0.24
Nodes (9): DecisionKind, PolicyDecision, PolicyGuard, Policy Guard — identity, scope, sensitivity, approval, loop limits., Deterministic authorization matrix before any tool side effect., Tool registry and connector adapters., Deterministic tool discovery, authorization handoff, invoke, audit., ToolCall (+1 more)

### Community 3 - "Community 3"
Cohesion: 0.27
Nodes (8): Enum, FeedbackNormalizer, FeedbackRecord, FeedbackType, Structured human feedback — first-class learning signal., Validate and persist UI feedback into the feedback table., RunStatus, str

### Community 4 - "Community 4"
Cohesion: 0.33
Nodes (5): EvalResult, EvaluationEngine, Independent evaluation — is the candidate actually better?, Score candidates against benchmark datasets; never trusts Evolution alone., Scorecard

### Community 5 - "Community 5"
Cohesion: 0.29
Nodes (4): IngestWorker, Company knowledge retrieval — Postgres + pgvector (not Graphify)., Chunk and embed uploaded documents into knowledge_chunks., RetrievedChunk

### Community 6 - "Community 6"
Cohesion: 0.25
Nodes (5): Orchestrator, PlannerRouter, Hybrid router: policy tables first, LLM only when ambiguous., Owns session/task lifecycle, budgets, and tracing hooks., Enqueue a run; returns run_id.

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolRegistry` connect `Community 0` to `Community 2`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `VersionStatus` connect `Community 1` to `Community 3`, `Community 4`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Why does `TaskRequest` connect `Community 0` to `Community 6`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `ToolRegistry` (e.g. with `AgentAnswer` and `AgentVersionConfig`) actually correct?**
  _`ToolRegistry` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `PolicyGuard` (e.g. with `AgentAnswer` and `AgentVersionConfig`) actually correct?**
  _`PolicyGuard` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Retriever` (e.g. with `AgentAnswer` and `AgentVersionConfig`) actually correct?**
  _`Retriever` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `OpsAgent` (e.g. with `Retriever` and `RouteDecision`) actually correct?**
  _`OpsAgent` has 5 INFERRED edges - model-reasoned connections that need verification._