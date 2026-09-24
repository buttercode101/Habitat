# Habitat — Current State

> Canonical restart point. Read this before making a material change.

**Last reconciled:** 2026-09-24  
**Repository:** `buttercode101/Habitat`  
**Default branch:** `main`  
**HEAD:** pending 10× integration commit  
**Package version:** `1.3.0`  
**Python:** `>=3.10`  
**Runtime dependencies:** none; optional Ed25519 signing dependency  
**License:** MIT

## What Habitat is today

Habitat is a local-first supervision and accountability runtime for autonomous agents. It records structured agent/job activity, maintains a trusted local ledger, correlates claims to runs, evaluates evidence and policy, raises supervision signals, and exports portable proof bundles for independent verification.

The current product is **Habitat**. Forge / project-truth-layer remains a product hypothesis discovered during validation; it is **not shipped functionality**.

## 2026-09-24 10× integration

The current state now includes the Habitat 10× package, applied within the existing product boundary:

- optional local external tip anchoring via `habitat.anchor`
- Hermes post-action/in-process bridge and signed HMAC event adapter
- reusable evidence-policy presets for run binding, drift/skip rejection, auth outcomes, and evidence freshness
- read-only agentscope proof source plus integration instructions/config
- CI workflow for proof + optional tip verification
- release-proof / handoff / rescue monetization artifacts as explicit hypotheses, not traction claims

### Assurance boundary

The verifier now distinguishes:

- structural validity
- content integrity
- internal consistency
- signature presence/cryptographic validity
- publisher trust
- external-world truth

A signature that verifies cryptographically is **not** automatically publisher-trusted. Trust requires an explicit trust registry.

### Integration boundary

- Hermes integration is production-shaped but **not claimed as live production wiring** until exercised against a real Hermes installation.
- agentscope integration is read-only and documented; its separate repository is **not claimed as merged**.
- tip anchoring is local-first and optional; no external anchoring service is assumed.
- monetization material is a testable cashflow hypothesis, not evidence of paying customers.

## Verified repository facts

- `main` is the default branch and the repository is public and unarchived.
- Package version is `1.3.0` with no required runtime dependencies.
- SQLite is the durable local store.
- OTel-style GenAI spans can be bridged into Habitat using an existing trace ID as Habitat run ID.
- Claims can be bound to exact runs/correlations and checked against recorded evidence.
- The action ledger has tamper-evident SHA-256 chaining and integrity checks.
- Portable proof bundles can be exported and verified without the producer's database, server, or Habitat installation.
- Optional Ed25519 signing and an explicit trust registry exist; signature presence, cryptographic verification, publisher trust, and external-world truth are separate assurance levels.
- A standalone GitHub Actions proof-verification workflow is now included.
- Public site: `https://habitat-za.vercel.app`.

## Immediate next action

**Verify the integrated state before feature expansion.** Run the core suite, the anchor tests, the proof-signature assurance regression, Hermes local prove smoke, and the web deployment/route checks. Record discrepancies before adding features.

## Anti-drift rule

> **Never make the project look more complete than it actually is.**

No fake functionality, metrics, verification, security claims, or undocumented assumptions.
