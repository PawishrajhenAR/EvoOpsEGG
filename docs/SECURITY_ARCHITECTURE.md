# EvoOps Security Architecture

EvoOps secures a **single-org** IT triage demo where LLMs propose actions and config changes but **cannot expand privilege** without admin-defined policy and human approval. Security is layered: **Supabase Auth + RLS**, **Policy Guard**, **tool authorization matrix**, **prompt/injection defenses**, and **gated promotion** for evolved config.

**Invariant:** No LLM path may grant itself new tool scopes, connector secrets, or RLS-bypass capabilities.

---

## Threat model (MVP)

| Threat | Vector | Primary control |
|--------|--------|-----------------|
| Prompt injection | Ticket body instructs model to exfiltrate | Policy Guard, output scanning, retrieval citations only |
| Tool abuse | Model selects destructive action | Allowlists, risk classes, approval gates |
| Privilege escalation | Operator promotes malicious version | Approver role + eval gates + safety linter |
| Cross-role data leak | Operator reads approver-only rows | RLS policies |
| Credential theft | Logs or LLM context | Server-side secrets only, redaction |
| MCP dev bypass | Local MCP with write tools | `MCP_ENABLE_WRITE`, same audit trail |
| SQL injection | Adapter query construction | Parameterized SQL / RPC only |

Out of scope for MVP: multi-tenant isolation, SOC2 certification, HSM key storage.

---

## Identity & roles

| Role | Capabilities |
|------|--------------|
| `operator` | Run triage UI, submit feedback, view runs for assigned queues |
| `approver` | All operator + approve/reject agent versions, view eval reports |
| `admin` | Connector enablement, semantic ingest, rollback, user role assignment |

Auth: Supabase JWT on web and API. Service role confined to worker processes with **minimal** SQL surface via adapters.

---

## Row Level Security (RLS)

All operational tables enable RLS. Patterns:

| Table pattern | SELECT | INSERT | UPDATE |
|---------------|--------|--------|--------|
| `tasks`, `task_runs`, `run_events` | operators: org + queue membership; admin: all | system workers via service role | system only |
| `feedback` | operators own + aggregate read | operators insert own | none |
| `agent_versions` | all roles read non-secret fields | system (proposer) | Promotion Service |
| `approvals` | approver+ | approver+ | none |
| `audit_log` | approver+ read; append-only | service role insert | none |
| `semantic_chunks` | all authenticated read active | admin ingest | admin |
| `tool_calls` | operators related runs | Invoke Service | status fields only |

**Queue membership:** `operator_queue_grants(operator_id, queue)` drives task visibility.

Service role bypass is **not** exposed to Ops Agent or MCP tools—adapters enforce row filters equivalent to RLS semantics.

---

## Tool authorization matrix

Scopes are strings checked by Policy Guard. Connectors declare `required_scopes` per action.

### Scope catalog

| Scope | Meaning |
|-------|---------|
| `tool:read:tasks` | Read task summaries via adapter |
| `tool:write:task_notes` | Append operator/system notes |
| `tool:notify:email` | Resend send to allowlisted domains |
| `tool:mock_it:read` | Fetch mock IT queue/status |
| `tool:mock_it:write` | Update mock ticket status |
| `tool:mock_it:inject` | Inject demo tickets (**admin** only) |
| `tool:admin:connectors` | Enable/disable connectors |

### Role × scope (default matrix)

| Scope | operator | approver | admin |
|-------|----------|----------|-------|
| `tool:read:tasks` | ✓ | ✓ | ✓ |
| `tool:write:task_notes` | ✓ | ✓ | ✓ |
| `tool:notify:email` | ✓ | ✓ | ✓ |
| `tool:mock_it:read` | ✓ | ✓ | ✓ |
| `tool:mock_it:write` | ✓ | ✓ | ✓ |
| `tool:mock_it:inject` | ✗ | ✗ | ✓ |
| `tool:admin:connectors` | ✗ | ✗ | ✓ |

### Action × risk class × default policy

| action_id | risk_class | Default operator policy | Approval required |
|-----------|------------|-------------------------|-------------------|
| `supabase.query_read` | read | ALLOW | No |
| `supabase.upsert_task_note` | write | ALLOW | No |
| `resend.send_ops_email` | notify | ALLOW (domain allowlist) | No for internal; Yes for external domain |
| `mock_it.fetch_queue` | read | ALLOW | No |
| `mock_it.update_ticket_status` | write | ALLOW | No in demo |
| `mock_it.inject_demo_ticket` | write | DENY | Admin only |

**Evolution constraint:** `tool_policy` diffs may only **narrow** or **explicitly allow** actions already in manifest; adding `mock_it.inject_demo_ticket` to operator allowlist is rejected by Safety stage.

---

## Policy Guard

Evaluation order (short-circuit on DENY):

1. **Authentication** — valid JWT or system worker identity.
2. **Role scopes** — matrix above.
3. **Agent version tool_policy** — allow/deny/require_approval lists.
4. **Argument validation** — JSON Schema + size limits.
5. **Injection heuristics** — see below.
6. **Rate limits** — per action / per run.
7. **Approval token** — if `REQUIRE_APPROVAL`, valid `approval_requests` row must exist.

Decisions persisted on `tool_calls.policy_decision` before invoke.

---

## Injection & untrusted content defenses

### Input sources (untrusted)

- Ticket email body, attachments text, mock IT fields
- Operator free-text comments
- Retrieved semantic chunks (lower trust than system prompts)

### Defenses

| Layer | Control |
|-------|---------|
| Retrieval | Citation-only chunks; strip HTML; max tokens |
| Ops Agent system prompt | Fixed instructions: ignore override commands in ticket |
| Tool args | Schema validation; block URLs not in allowlist; block `SELECT` in string fields |
| Pre-invoke scan | Deny if args match `ignore previous`, `system prompt`, `curl`, `api_key` patterns (tunable) |
| Post-output scan | Secret regexes (OpenAI keys, JWT eyJ..., `service_role`) |
| Eval | `safety.no_secret_leak` gate |

LLM **never** receives raw service role key or Resend API key in context.

---

## Approval gates

| Action | Gate type |
|--------|-----------|
| Tool call with `require_approval` | Inline approval request (approver UI) |
| Agent version promotion | Eval pass + approver record |
| Connector enablement | Admin + audit |
| External email domain | Policy flag → approval |
| MCP write tools | Env + optional admin token |

**No auto-approve** for evolution in MVP.

---

## LLM scope boundary (critical)

| Allowed | Forbidden |
|---------|-----------|
| Choose among registered `action_id`s | Register new actions at runtime |
| Fill tool args within schema | Mutate `connectors` table |
| Draft config patches in evolution | Apply `ACTIVE` without Promotion Service |
| Suggest playbook text in proposal | Write directly to `semantic_chunks` in prod |

Enforcement: Tool Registry static manifests; Promotion Service transaction; Evolution schema denylist; code review for Agent F generated adapters.

**Admin** may change scopes and policies via UI/migrations—not via Ops Agent chat.

---

## Audit & logging

**Table:** `audit_log`

| Field | Content |
|-------|---------|
| `event_type` | e.g. `tool.invoke`, `policy.denied`, `agent_version.promoted` |
| `actor_id` | user or `system:worker` |
| `resource_type` / `resource_id` | |
| `payload` | redacted jsonb |
| `correlation_id` | |

Retention: 1 year demo default. Immutable append-only (no UPDATE/DELETE for non-admin break-glass).

Langfuse: no PII in trace names; scrub ticket bodies in exported spans optional flag.

---

## Secrets management

| Secret | Location |
|--------|----------|
| Supabase service role | Worker env (Railway/Render) |
| OpenAI API key | Worker env |
| Resend API key | Worker env |
| Mock IT HMAC | Worker + webhook config |

Never in: `agent_version_config`, client-side Next.js bundle, Graphify output committed to git (Agent L scans).

---

## Network & deployment

| Component | Exposure |
|-----------|----------|
| Next.js | Public Vercel |
| FastAPI | HTTPS, JWT required |
| Workers | Private network / same service |
| Supabase | Public API with RLS |
| MCP dev server | localhost only by default |

CORS: web origin allowlist. Rate limit auth endpoints.

---

## Eval & evolution safety

Cross-reference [Evaluation System](EVALUATION_SYSTEM.md):

- Blocking gates on policy and secret scan.
- Safety stage after eval: denylist paths, prompt lint, tool policy monotonicity option.

Cross-reference [Evolution Engine](EVOLUTION_ENGINE.md):

- Forbidden mutation of credentials and RLS.

---

## Incident response (demo)

| Event | Response |
|-------|----------|
| Spike `policy_denied` | Review ticket sample; tighten heuristics |
| Suspected leak in output | Rollback agent version; rotate keys |
| Bad promotion | Rollback + mark pattern `DISMISSED` |

---

## Security checklist (release)

- [ ] RLS enabled on all new tables (Agent J)
- [ ] Matrix row for each new manifest action (Agent H)
- [ ] Policy Guard tests for DENY paths (Agent D)
- [ ] Eval golden includes injection cases
- [ ] MCP write disabled in prod images
- [ ] Audit log entries for promote/rollback

---

## Related documents

- [MCP Architecture](MCP_ARCHITECTURE.md) — MCP/prod parity
- [Agent Architecture](AGENT_ARCHITECTURE.md) — Policy Guard, Promotion Service
- [Evolution Engine](EVOLUTION_ENGINE.md) — safety stage
- [Evaluation System](EVALUATION_SYSTEM.md) — regression gates
