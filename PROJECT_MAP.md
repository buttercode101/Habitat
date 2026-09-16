# Habitat — Project Map

This is the canonical map of the project as reconstructed from the repository, its documentation, and the recent Git history. It deliberately separates implemented Habitat work from the later Forge discovery so future sessions do not collapse them into one thing.

## 1. Project lineage

```text
Habitat concept
    ↓
minimal local-first runtime / supervision
    ↓
structured state + actions + signals
    ↓
agent identity / authorization / protocol hardening
    ↓
evidence + claims + verification
    ↓
tamper-evident ledger
    ↓
portable proof exchange
    ↓
signed proof + trust model
    ↓
real-project proof demonstrations
    ↓
public landing / live proof surface
    ↓
responsive web hardening
    ↓
market + competitive red-team
    ↓
Forge / Project Truth Layer hypothesis
    ↓
CURRENT: stabilize the map before the next product decision
```

## 2. Habitat — implemented product

### Original product thesis
Habitat began as a small, local-first home/supervision layer for autonomous agents: keep structured state, record actions, surface anomalies, and let humans intervene when needed.

The repository's original product definition explicitly rejected becoming a multi-agent orchestration framework, heavy tracing platform, visual agent builder, or replacement for existing agent frameworks.

### Runtime foundation
The runtime evolved around:
- jobs and runs;
- state;
- structured actions/events;
- supervision signals;
- recovery hooks/lifecycle;
- scheduling;
- SQLite persistence;
- CLI and HTTP supervision surface;
- diagnostics and backup/restore.

### Security and protocol hardening
The project then added:
- agent registry and least-privilege authorization;
- secure structured event ingestion;
- exact run/correlation binding;
- HMAC request signing;
- identity lifecycle rules;
- key binding;
- typed external evidence predicates;
- tamper-evident SHA-256 action chaining;
- corruption/integrity refusal paths;
- explicit security boundaries.

### Evidence / verification evolution
The core question sharpened from supervision toward accountability:

> When an agent says it did something, what evidence does Habitat actually have for that statement?

This led to:
- claim objects;
- evidence requirements;
- deterministic evidence policies;
- claim-to-run/action consistency;
- verification results;
- explicit assurance levels;
- portable proof bundles;
- compact proof cards;
- a standalone verifier;
- GitHub Actions verification;
- optional Ed25519 signing;
- a TrustRegistry with expiry/revocation semantics.

### Real-work demonstrations
The repository history records proof work around real projects including Rosendaltown, SoloBid-v2, Diketo, and Greenlight. Temporary proof workflows were removed after the demonstrations, while durable proof examples/documentation remained.

### Public product surface
The project gained a public landing page and a separate operational inspection surface. The landing page was iteratively polished, with the real proof artifact made the central demonstration rather than relying on fake product metrics or a simulated dashboard.

The most recent changes before this map were focused on responsive behavior and removal of competing/obsolete responsive stylesheets.

## 3. Forge discovery — NOT current implementation

During the long validation thread, we asked a larger question:

> How can an AI-assisted software project maintain an evidence-backed understanding of what is actually true as agents, developers, sessions, code, environments, and releases change?

This became the **Project Forge** concept.

The initial Forge framing was broader than Habitat:
- project takeover;
- build/change/verify workflow;
- durable project state;
- agent handoff;
- project rescue;
- verification/attestation;
- eventual CLI/cloud possibilities;
- transaction-based monetization around trust events.

## 4. Forge red-team findings

The original Forge positioning was deliberately attacked rather than protected.

### Killed / weakened
- "AI code auditor" — crowded.
- "AI coding agent" — crowded and not the intended layer.
- "AI project manager" — wrong abstraction.
- generic agent handoff/continuity — multiple products already exist.
- generic verification — multiple products and research projects already exist.
- "Project Forge" as a name — too crowded; multiple public projects use Forge/Project Forge.
- hash chains, signatures, JSON proof files, and audit trails as standalone moats — increasingly table stakes.

### Surviving hypothesis
A stronger hypothesis emerged:

> A software project may need a durable, evidence-backed state that distinguishes what is verified, inferred, claimed, stale, and unknown — and that state should remain useful across agents, humans, sessions, changes, releases, and handoffs.

Temporary working language included **Project Truth Layer**. This is a hypothesis, not a product decision.

## 5. Validation hypotheses

### H1 — Reality
Project documentation, agent memory, intended state, and actual project state can diverge materially.

### H2 — Evidence
Knowing why a statement is considered true may have value beyond a prose summary.

### H3 — Continuity
Evidence/state may need to survive agent and developer changes, sessions, branches, releases, and handoffs.

### H4 — Actionability
A useful truth layer must change what agents/humans do; another passive report is insufficient.

### H5 — Economic value
A concrete outcome such as a verified release, handover, rescue, assurance package, or due-diligence artifact may have transactional value.

## 6. Validation experiments proposed

1. **Cold takeover:** compare an agent taking over unfamiliar repositories with and without evidence-backed state.
2. **Truth decay:** intentionally change repositories after claims are verified and test whether stale evidence is detected.
3. **Agent switching:** test Claude → Codex → Cursor → Gemini style handoffs using only repository + durable state.
4. **Broken-project rescue:** expose contradictory/stale documentation, failing tests, mismatched deployments and incomplete features; ask what is actually true before changing anything.
5. **Buyer test:** test the usefulness of evidence packages with founders, developers, agencies, CTOs and technical diligence contexts.

None of these experiments should be described as completed unless results are actually recorded.

## 7. Competitive map — current interpretation

| Area | Existing market | What it means for Habitat / future Truth Layer |
|---|---|---|
| Observability/evals | LangSmith, Langfuse, Phoenix, AgentOps and others | Integrate; do not rebuild general tracing/evals |
| Coding agents | Claude Code, Codex, Cursor, Copilot, Devin, etc. | Sit above/beside agents rather than competing on code generation |
| Review/validation | Qodo, Greptile, Copilot review and others | Do not claim generic AI review as differentiation |
| Handoff/continuity | OSTK, Stateora, Conductor, HandoffKit and others | Handoff alone is not enough |
| Provenance/evidence | Aevum, Hashirai, AgentProvenance, related research | Portable evidence primitives are not unique |
| Technical diligence | CodeDD, human audit services and others | Demonstrates economic value of technical clarity, but is a different workflow |
| Project auditing | SystemAudit and emerging audit kits | Repository diagnosis is adjacent, not the whole thesis |

The existing `COMPETITIVE_INTELLIGENCE.md` is the authoritative repository snapshot for this market research and should be refreshed when new decisions depend on it.

## 8. Business hypotheses

Potential economic events identified during validation:
- verified handover;
- production-release verification;
- investor technical evidence package;
- acquisition/due-diligence evidence;
- project rescue;
- incident evidence reconstruction.

Subscription/seat pricing was deliberately not accepted as the default business model. Transactional value is a hypothesis to test.

## 9. Important separation

```text
FACT
  = backed by current repository evidence

DECISION
  = deliberately chosen direction

HYPOTHESIS
  = plausible but unproven

EXPERIMENT
  = test designed to resolve a hypothesis

UNKNOWN
  = not established

REJECTED
  = deliberately ruled out for stated reasons
```

Never promote a hypothesis to a fact merely because it has been discussed repeatedly.

## 10. Where we are now

Habitat is a real, implemented repository with a mature evidence/proof direction and a public surface. Forge/Truth Layer is a discovery that deserves disciplined validation, but it has not earned a rename, rewrite, or major architectural pivot.

The next work unit is therefore **reconciliation and verification**, not feature expansion.
