# Habitat — Current State

> Canonical restart point. Read this before making a material change.

**Last reconciled:** 2026-09-25  
**Repository:** `buttercode101/Habitat`  
**Default branch:** `main`  
**Package version:** `1.3.0`  
**Python:** `>=3.10`  
**Runtime dependencies:** none; optional Ed25519 signing dependency  
**License:** MIT

## What Habitat is today

Habitat is a local-first supervision and accountability runtime for autonomous agents. It records structured agent/job activity, maintains a trusted local ledger, correlates claims to runs, evaluates evidence and policy, raises supervision signals, and exports portable proof bundles for independent verification.

The current product is **Habitat**. Forge / project-truth-layer remains a product hypothesis discovered during validation; it is **not shipped functionality**.

## Verified live state

- `main` is the default branch and the repository is public and unarchived.
- `https://habitat-za.vercel.app` was browser-verified after the repository became public.
- Landing, dashboard, proof interaction, tamper simulation, reset, JSON download, responsive behavior and the GitHub CTA were exercised successfully.
- The GitHub CTA reaches the public canonical repository.
- GitHub Actions on commit `aa1a6f25fd8a6f970e8b40f540d4c44d24ee37d9` passed on Python 3.10, 3.11, 3.12, 3.13 and dependency audit.
- The dashboard explicitly discloses that the live backend is unavailable and falls back to checked-in demo proof; it is not presented as live backend data.

## 10× integration boundary

- optional local external tip anchoring via `habitat.anchor`
- Hermes bridge/adapter is production-shaped but not claimed live until exercised against a real Hermes installation
- reusable evidence-policy presets
- read-only AgentScope proof source/integration guidance
- proof + optional tip verification workflows
- monetization material remains hypothesis, not traction

## Reconciliation finding

The live verification did not exercise the Evidence archive route. Repository inspection then found that the previous public archive contained stale/mislabeled proof paths: multiple paths pointed to identical payloads whose claim/run identity belonged to a different project. The previous “22 proofs / 8 projects” presentation was therefore not safe to claim as evidence.

The public Evidence surface and manifest have now been narrowed to the two artifacts whose checked-in path, run ID and claim were directly reconciled during this pass. The remaining historical proof paths are deliberately excluded rather than relabeled or replaced with invented evidence.

## Assurance boundary

The verifier distinguishes structural validity, content integrity, internal consistency, signature presence/cryptographic validity, publisher trust, and external-world truth. A cryptographically valid signature is not automatically publisher-trusted.

## Current gate

The corrected Evidence route and manifest have been independently browser-verified, and the current CI matrix is green on Python 3.10–3.13 plus dependency audit. The reproducible project-state workflow is now documented in `PROJECT_STATE.md` and `HANDOFF.md`.

## Remaining validation

The Truth Layer experiments remain deliberately open: cold takeover, truth decay, agent switching, broken-project rescue, and buyer/economic-value testing. They are not product features and must not be described as completed until executed with recorded evidence.

## Anti-drift rule

> **Never make the project look more complete than it actually is.**

No fake functionality, metrics, verification, security claims, or undocumented assumptions.
