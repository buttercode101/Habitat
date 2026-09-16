# Habitat — Current State

> Canonical restart point. Read this before making a material change.

**Last reconciled:** 2026-09-16  
**Repository:** `buttercode101/Habitat`  
**Default branch:** `main`  
**HEAD:** `35e7fdf820ace8b5cb31b4f5838be8e468340aa5`  
**Package version:** `1.3.0`  
**Python:** `>=3.10`  
**Runtime dependencies:** none; optional Ed25519 signing dependency  
**License:** MIT

## What Habitat is today

Habitat is a local-first supervision and accountability runtime for autonomous agents. It records structured agent/job activity, maintains a trusted local ledger, correlates claims to runs, evaluates evidence and policy, raises supervision signals, and can export portable proof bundles for independent verification.

The current product is **Habitat**. The later **Forge / project-truth-layer** idea is a product hypothesis discovered during validation; it is **not currently the implemented product and must not be treated as shipped functionality**.

## Verified repository facts

- `main` is the default branch and the repository is public and unarchived.
- The package is version `1.3.0` with no required runtime dependencies.
- SQLite is the durable local store.
- OTel-style GenAI spans can be bridged into Habitat without adding another tracing protocol.
- Claims can be bound to exact runs/correlations and checked against recorded evidence.
- The action ledger has tamper-evident SHA-256 chaining and integrity checks.
- Portable proof bundles can be exported and verified without the producer's database, server, or Habitat installation.
- Optional Ed25519 signing and an explicit trust registry exist; signature presence, cryptographic verification, publisher trust, and external-world truth are intentionally separate assurance levels.
- A standalone GitHub Actions proof-verification workflow exists.
- A public landing site is documented as `https://habitat-za.vercel.app`.

## Current implementation areas

### Runtime / protocol
- configuration and validation
- SQLite persistence
- jobs and run correlation
- structured events and authenticated HTTP ingestion
- agent identity and authorization
- actions / claims / evidence
- supervision signals and recovery lifecycle
- scheduling loop
- external evidence predicates
- doctor diagnostics
- backup / restore
- CLI

### Assurance / proof
- tamper-evident action ledger
- claim verification
- deterministic evidence policies
- portable `proof.json` bundles
- compact proof cards
- standalone zero-install verifier
- optional Ed25519 signatures
- trusted-key registry with expiry/revocation
- explicit assurance model

### Interoperability
- OTel-style bridge using an existing trace ID as Habitat run ID
- intentionally small accountability projection rather than a replacement telemetry protocol

### Public surface
- public landing page
- live proof artifact as the core marketing demonstration
- separate operational inspection surface
- responsive/mobile hardening work through the current HEAD

## What is *not* verified by this state file

This file does not claim that every production deployment, external service, real-world outcome, or security property has been independently re-tested today. It records repository facts and documented boundaries. Runtime verification must still be performed where the task depends on it.

## Known current focus

The last repository changes were concentrated on the public web surface and responsive cleanup. The current HEAD removes an obsolete competing responsive stylesheet. Before feature work resumes, the next agent should verify the working tree/CI state and reconcile the public surface with the current implementation.

## Immediate next action

**Do not add product features yet.** Perform a baseline verification pass against HEAD: repository tree, tests/CI, web build/deploy state, proof verification paths, and documentation consistency. Record discrepancies before changing code.

## Restart protocol

1. Read `PROJECT.md`.
2. Read this file.
3. Read `PROJECT_MAP.md` for the historical/product map.
4. Read `DECISIONS.md` before revisiting a disputed direction.
5. Read `ROADMAP.md` before proposing new work.
6. Inspect the actual repository at the current HEAD.
7. Treat `VERIFIED` facts as repository-backed; treat `HYPOTHESIS`, `ASSUMPTION`, and `UNKNOWN` explicitly.
8. After material work, update this file and the relevant decision/roadmap record in the same change.

## Anti-drift rule

> **Never make the project look more complete than it actually is.**

No fake functionality, fake metrics, fake verification, fake security claims, or undocumented assumptions. If something is not verified, label it.
