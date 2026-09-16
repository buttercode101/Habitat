# Habitat — Work History Map

This is a compact reconstruction of the work arc. It is intentionally phase-based rather than pretending every chat message or commit is a product decision.

## Phase 1 — Habitat foundation

Habitat was established as a minimal local-first supervision/runtime concept for autonomous agents, centered on structured state, actions, signals, recovery and human supervision.

## Phase 2 — Runtime hardening

The implementation expanded into durable SQLite state, jobs/runs, structured events, HTTP ingestion, agent registry/authorization, signals, scheduling, external evidence predicates, diagnostics and backup/restore. Shell execution and packaging were hardened.

## Phase 3 — Accountability model

The project sharpened around a stronger question: an agent can report an action, but what evidence supports the report? Claim binding, evidence checks, run correlation and tamper-evident action history were added.

## Phase 4 — Proof exchange

Portable proof bundles and a zero-install verifier were added so a recipient can validate a proof artifact without the producer's database or service. Assurance levels were made explicit so integrity, authenticity, trust and external truth are not conflated.

## Phase 5 — Cryptographic trust

Optional Ed25519 signing and a trusted-key registry were added, with key expiry/revocation and agent/key binding. The project intentionally retained explicit trust boundaries rather than presenting signatures as universal truth.

## Phase 6 — Real-project demonstrations

Proof workflows were exercised against real work including Rosendaltown, SoloBid-v2, Diketo and Greenlight. Temporary workflow scaffolding was removed after use; durable examples and proof-card documentation remained.

## Phase 7 — Public product surface

A public Habitat landing page was introduced, made indexable/share-ready, and separated from the operational inspection dashboard. The real proof artifact became the central demonstration. The site then received multiple rounds of high-craft/premium marketing and responsive work.

## Phase 8 — Responsive cleanup

The most recent commit sequence concentrated on small-screen navigation/layout, viewport safety, stylesheet precedence, and removal of obsolete competing responsive stylesheets. Current HEAD is `35e7fdf820ace8b5cb31b4f5838be8e468340aa5`.

## Phase 9 — Competitive intelligence

Market research showed that general observability, agent governance, handoff/continuity, provenance, project auditing and verification are all becoming active categories. The repository now records this conservatively in `COMPETITIVE_INTELLIGENCE.md`.

## Phase 10 — Forge discovery

The team explored a broader product abstraction initially called **Project Forge**: a system that could understand, change, verify and hand off software projects across agents. The discussion produced ideas around project state, verification, rescue, handoff, attestation and transaction-based monetization.

## Phase 11 — Forge red-team

The name and several positioning claims were attacked. "Forge" was found to be crowded. Generic AI auditing, handoff, continuity and verification were also found to have significant competition. The surviving hypothesis became a broader **evidence-backed project truth/state** concept.

## Phase 12 — Current pause

The correct move is not to immediately turn Habitat into the new product. We are pausing feature expansion to reconcile the actual implementation, history, decisions, hypotheses and next experiments. This phase exists specifically to prevent the long-thread/context-loss problem from recurring.

## Evidence rule

This history is reconstructed from repository artifacts and recent Git history. It is a project map, not a verbatim transcript. If a future claim needs exact commit-level provenance, inspect GitHub history for that claim rather than treating this narrative as exhaustive.
