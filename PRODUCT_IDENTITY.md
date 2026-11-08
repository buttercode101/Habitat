# Habitat — Product Identity (Phase 1)

**Date:** 2026-11-08
**Repo:** `buttercode101/Habitat` @ `fb8aefe7` (local clone `~/habitat-audit`)
**Live:** https://habitat-za.vercel.app
**Package:** `habitat 1.3.0`, MIT, Python ≥3.10, zero runtime deps (+ optional `cryptography` for Ed25519)

> This file separates **Evidence** (directly observed in repo / live site on 2026-11-08) from **Hypotheses** (unvalidated beliefs) and **Unknowns**. Do not promote a hypothesis to a fact.

---

## 1. Evidence — What Habitat is

### 1.1 One-line definition (verbatim, README + live hero)

> **A local-first supervision and evidence runtime for autonomous agents.**

Live hero (2026-11-08): *"Don't just log what an agent did. Prove it."* — *"Habitat turns agent events into policy-checked claims and portable proof artifacts you can inspect, verify and carry outside the system that produced them."*

Secondary phrasing in repo (`PROJECT.md`): *"A minimal, self-observing home for autonomous agents."*

### 1.2 The question it answers

> **What evidence does the system actually have for that claim?** (README "Why Habitat exists")

Not: what happened (observability), how to build agents (frameworks), or whether the outside world matches the claim (external truth).

### 1.3 Core model (Evidence: `README.md`, `ARCHITECTURE.md`, `OTEL.md`, `PROTOCOL.md`)

```text
Agent → Event → Habitat ledger → Integrity → Verification → Signal → Human
                         ↓
                       SQLite
```

Four stages, each a distinct module:

| Stage | What it does | Source |
|---|---|---|
| **Capture** | Receive `POST /v1/events` (JSON, HMAC-signed by default), bind to `habitat_id` + `agent_id` + `run_id`; reject duplicates by persistent event ID | `habitat/events.py`, `server.py`, `PROTOCOL.md` |
| **Check** | Least-privilege agent authorization, identity lifecycle (`active→disabled→active`, `→revoked` terminal), key binding, tamper-evident SHA-256 hash-chained action ledger | `identity.py`, `trust.py`, `store.py`, `IDENTITY.md`, `SECURITY.md` |
| **Correlate + Verify** | Claims require `run_id`/`correlation_id`; deterministic `EvidencePolicy` (typed expected fields/status) + ledger-integrity gate → `verified` / `inconclusive` (never auto-upgraded) | `claims.py`, `verify.py`, `policy.py`, `policy_presets.py` |
| **Prove** | Export portable JSON proof bundle (`proof_version=1`, `content_sha256` over canonical JSON excl. `generated_at` and optional `signature`) + human proof card; optional Ed25519 signing; optional local tip anchoring (`habitat.anchor`) | `proof.py`, `proof_card.py`, `proof_sign.py`, `anchor.py`, `schemas/proof-v1.schema.json` |

### 1.4 What Habitat proves — and explicitly does not (Evidence: `README.md`, `PROOF.md`, `VERIFY_PROOF.md`, `SECURITY.md`)

**Can establish:**
- A matching action was recorded in the local ledger
- The ledger is internally consistent (hash-chain intact at verification time)
- A claim matches an exact run when a run ID is supplied
- An explicit external evidence adapter (HTTP / shell) returned an expected result

**Does NOT establish:**
- That an agent's private reasoning was correct
- That a compromised host is trustworthy
- That the local SQLite DB is independently anchored cryptographic truth
- External-world truth, publisher trust, or key custody — these are separate, explicitly separated assurance levels

**Six-level assurance model** (the product's signature discipline — `VERIFY_PROOF.md`, `SIGNING.md`):
`structural_validity` → `content_integrity` → `internal_consistency` → `signature` (`absent` / `present-unverified` / verified) → `publisher_trust` (requires independent `TrustRegistry`) → `external_truth` (always `not-established` by verifier alone).

### 1.5 What Habitat is not (Evidence: `PROJECT.md`, `README.md`, `ADOPTION.md`)

- ❌ Not an orchestration platform / multi-agent framework (not a LangGraph/CrewAI replacement)
- ❌ Not a general tracing/observability platform (integrates with OTel; does not replace LangSmith/Langfuse/Phoenix/AgentOps)
- ❌ Not a visual agent builder
- ❌ Not a blockchain project, generic IAM replacement, or hosted SaaS control plane
- ❌ Not a runtime firewall pretending to be an evidence system
- ❌ Not a compliance product claiming real-world truth

### 1.6 Architecture & stack (Evidence: `pyproject.toml`, `habitat/*.py` — 2,898 LOC across 27 modules)

- **Runtime:** Python stdlib only. SQLite (`store.py`, 302 LOC), WAL + foreign keys. HTTP server binds `127.0.0.1:8787` by default.
- **CLI (`habitat`):** `init`, `run [--watch]`, `status`, `inspect`, `serve`, `event`, `claim`, `verify`, `proof`, `prove`, `agent-add`, `agents`, `doctor`, `backup`, `restore`, `generate` (`__main__.py`, 428 LOC).
- **Event protocol v1:** `id` (unique), `type` (`job.started/completed/failed`, `agent.heartbeat`, `claim.submitted`), `habitat_id`, optional `job_id`/`run_id`/`agent_id`/`error`. 256 KiB body cap. HMAC-SHA256 over exact UTF-8 body in `X-Habitat-Signature` (`sha256=` accepted).
- **OTel bridge (`habitat/otel.py`, 74 LOC, dependency-free):** `events_from_spans()` projects only accountability-relevant ops (`invoke_agent`, `invoke_workflow`, tool calls); OTel `trace_id` → Habitat `run_id`. Ordinary model/debug spans stay in the user's existing backend.
- **External evidence adapters (`adapters.py`, 209 LOC):** HTTP (SSRF-hardened: HTTPS-only, no redirects/credentials, DNS pre-resolution, private/reserved-IP rejection, 1 MiB body cap) and shell (argv-parsed, no shell interpretation).
- **Signals (`signals.py`):** anomaly codes — `config_drift`, `auth_failure`, `failure_streak`, `disabled_but_expected`, `no_output_when_expected`, `tool_hallucination`, `budget_exceeded`.
- **Security:** PBKDF2-HMAC-SHA256 agent secrets (legacy SHA-256 auto-upgraded), constant-time HMAC, remote auth-failure throttling, strict JSON (rejects non-finite numbers), proof caps (16 MiB / 10,000 actions), timestamps must be timezone-aware.
- **Web (`web/`, Next.js + TypeScript):** landing page, `/dashboard` (proof inspector with tamper simulation), `/evidence` (manifest-backed proof archive), `/claims/[id]`, API routes proxying to local Habitat. **Live backend is unavailable** — dashboard explicitly falls back to checked-in demo proof (`STATUS.md`, `web/lib/demo-proof.json`).

### 1.7 Developer experience (Evidence: `examples/`, `tools/`, live site)

| Moment | Experience |
|---|---|
| Install | Zero runtime deps; `pip install habitat` (+ optional `habitat[signing]`). Python 3.10+. |
| First proof | `habitat prove --run-id run-42 --claim "deployed v1.2.3" -o proof.json --card` → `python tools/verify_proof.py proof.json` (stdlib-only, exit 0/1, single file to copy) |
| Proof exchange | Producer: `habitat proof <claim-id> --output proof.json` (writes *only* the bundle). Consumer: zero-install `tools/verify_proof.py` **or** `python examples/proof_exchange.py`. CI: GitHub Actions verifies checked-in `proof.json` without Habitat installed. |
| OTel adoption | `python examples/otel_bridge.py` — feed existing spans, no SDK/framework swap |
| Hermes | `examples/hermes_bridge.py`, `hermes_hmac_adapter.py`, `hermes_post_action.sh` — production-shaped, **not claimed live** against a real Hermes install |
| Examples | `prove_run.py`, `full_proof_flow.py`, `generate_sample_proof.py`, `simple.yaml` |

### 1.8 Proof artifacts in repo (Evidence: `proofs/`, live `/evidence`)

| Project | Claim | Artifact | External exec evidence |
|---|---|---|---|
| Greenlight-K53 | DB cache refresh + offline fallback | VERIFIED | GitHub Actions: success |
| Diketo | Low-end performance soft limits | VERIFIED | Vercel: success |
| Rosendaltown | Category/content image mapping | CHECKABLE | **UNVERIFIED** — commit not independently resolved |
| SoloBid-v2 | Invoice DueToday coverage + UI lanes | VERIFIED | Not exposed for historical SHA |

**Evidence discipline observed:** `STATUS.md` records that the prior public archive claimed "22 proofs / 8 projects" but contained stale/mislabeled paths (multiple paths → identical payloads for a different project). The public Evidence surface was narrowed to the 2 directly reconciled artifacts (`web/public/proofs/Diketo`, `Greenlight-K53`) + manifest. Historical artifacts remain in `proofs/quarantine/` **excluded, not relabeled**. Live Rosendaltown hero card correctly shows `UNVERIFIED` for the external commit.

### 1.9 Maturity (Evidence: GitHub API extract 2026-11-08, `git log`)

- 484 commits, 14 branches, 1 tag (`v1.3.0`), 0 stars / 0 forks / 1 contributor. MIT.
- CI: Python 3.10–3.13 + dependency audit (`test.yml`). Latest commit `fb8aefe` ("add npm dependabot coverage") shows a **failure** badge in the extract — current CI state needs re-verification.
- 27 test files covering ledger integrity, identity/signing, OTel, policy, proof verify, SSRF, standalone verifier, v04–v10 release gates.
- Changelog is sparse ("Unreleased" + one 2026-09-24 entry) — release-history discipline is weaker than code discipline.

### 1.10 Positioning statements used (Evidence: verbatim)

- *"Keep your agent framework and observability stack. Add Habitat when a claim needs evidence that another system can independently inspect."* (`ADOPTION.md`)
- *"A tiny, local-first accountability protocol that converts existing agent/OTel events into policy-checked claims and portable verification artifacts, without requiring a hosted control plane."* (`COMPETITIVE_INTELLIGENCE.md` — the defensible wedge)
- *"Logs tell you what was recorded. Proof tells you what the evidence supports."* (live site)

---

## 2. Target users

### Evidence-backed (who the product is built for today)
- Solo/small-team developers running autonomous agents locally who need to answer "did my agent actually do X?" for a consequential action (deploy, config change, workflow step) — evidenced by CLI-first UX, SQLite local-first, and the `habitat prove` flow.
- Engineers integrating an existing agent stack (LangChain/LangGraph, AgentScope, Hermes) who want a claim-verification layer without replacing observability — evidenced by OTel bridge, Hermes/AgentScope examples.

### Hypotheses (not yet validated — do not present as fact)
- **H-U1:** Teams hit a real "proof moment" (production change, audit, handoff, CI gate) often enough to adopt a separate evidence tool. *No user interviews, usage data, or customer evidence in repo.*
- **H-U2:** Auditors / downstream systems will consume the portable proof format. *No consumer adoption observed (0 stars/forks).*
- **H-U3:** The wedge buyer is a developer/DevOps engineer, not a compliance officer or enterprise platform team. *Untested.*

---

## 3. Business model status

**Evidence:** No pricing, packaging, or revenue material in repo. `DECISIONS.md` D-013: *"Transactional monetization is a hypothesis worth testing before seat-based SaaS"* (status: Experimental) — candidate trust events: verified handover, production-release verification, investor technical evidence package, acquisition due-diligence, project rescue, incident reconstruction. `PROJECT_MAP.md` §8 lists the same. **No traction claims are made anywhere in the repo** — correctly so.

---

## 4. Hypotheses & unknowns — kept separate

| ID | Statement | Status |
|---|---|---|
| H1–H5 (`PROJECT_MAP.md`) | Project docs/agent memory diverge from reality; evidence has value beyond prose; evidence must survive agent/handoff changes; a truth layer must change behavior; transactional value exists | All **unvalidated**; 5 experiments designed (cold takeover, truth decay, agent switching, broken-project rescue, buyer test), **none executed** |
| Forge / Project Truth Layer | Broader durable project-truth system built on Habitat primitives | **Hypothesis only** — explicitly not shipped; D-010/D-011 forbid rename/rewrite before validation |
| Hermes integration | Production-shaped bridge works against real Hermes | **Unknown** — not exercised (`STATUS.md`, `HANDOFF.md`) |
| Live backend | Dashboard serves live data | **False today** — checked-in demo proof fallback, disclosed on page (`STATUS.md`) |
| Market traction | Any customers/revenue | **None claimed; 0 GitHub stars** |

**Anti-drift rule (D-014, Permanent):** *"Never make the project look more complete than it actually is."* — No fake metrics, verification, or confidence. If unverified, say so.

---

## 5. Sources

Repo docs: `README.md`, `PROJECT.md`, `ARCHITECTURE.md`, `PROTOCOL.md`, `PROOF.md`, `VERIFY_PROOF.md`, `VERIFY.md`, `SIGNING.md`, `SECURITY.md`, `IDENTITY.md`, `OTEL.md`, `ADOPTION.md`, `SCHEMA.md`, `STATUS.md`, `PROJECT_MAP.md`, `DECISIONS.md`, `ROADMAP.md`, `HANDOFF.md`, `COMPETITIVE_INTELLIGENCE.md`, `proofs/README.md`, `examples/README.md`. Code: `habitat/*.py`, `pyproject.toml`, `web/`. Live site extract: habitat-za.vercel.app (2026-11-08). GitHub: buttercode101/Habitat (2026-11-08).
