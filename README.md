![CI](https://github.com/buttercode101/Habitat/actions/workflows/test.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

# Habitat

**A local-first supervision and evidence runtime for autonomous agents.**

Habitat records trusted agent actions, correlates work with run IDs, verifies claims against an evidence ledger or explicit external evidence, and produces portable proof that another machine can independently check.

[Live application](https://habitat-za.vercel.app) · [Quick start](#quick-start) · [Protocol](PROTOCOL.md) · [Security](SECURITY.md) · [Release verdict](RELEASE_VERDICT.md) · [MIT license](LICENSE)

## Current status — read this first

| | |
|---|---|
| **As a library + CLI + standalone verifier** | **Ready.** 116/116 tests green, `prove_run.py` → `VALID`, fresh-DB `demo → prove → verify` smoke green (2026-11-08). |
| **As a production evidence service** | **Not ready (73/100).** No production deployment, no key-management runbook, no authenticated access layer. The web dashboard is a **disclosed demo** — it falls back to checked-in demo proof because the live backend is unavailable. |
| **Traction / pricing** | **None claimed.** No users, revenue, or prices exist yet; see [MONETIZATION.md](MONETIZATION.md) — hypothesis only. |

The full, evidence-backed verdict (and what would change it) is in [RELEASE_VERDICT.md](RELEASE_VERDICT.md).
Five independent perspectives — developer, security, operator, buyer, maintainer — converge in [INDEPENDENT_REVIEW.md](INDEPENDENT_REVIEW.md).

> **Demo data is labelled as demo** — in CLI output, inside `proof.json` (`"sample": true`), on the proof card's
> assurance boundary, and on the dashboard. A `VERIFIED` demo proof means *"the claim matches evidence in the
> local ledger"* — never *"the claim is true in the world."*

## Why Habitat exists

Agents can report what they did. Habitat focuses on a narrower question:

> **What evidence does the system actually have for that claim?**

Habitat is not an orchestration platform, general tracing product, or replacement for an existing agent framework. It is an accountability and verification layer that can sit beside an agent runtime and existing telemetry.

## Core model

```text
Agent → Event → Habitat ledger → Integrity → Verification → Signal → Human
                         ↓
                       SQLite
```

The design is local-first, deterministic and intentionally explicit about what can and cannot be proven.

## What Habitat provides

- **Trusted action recording** in a local SQLite ledger.
- **Run correlation** using stable run IDs.
- **Integrity checks** over recorded actions.
- **Claim verification** against recorded evidence or explicit external evidence adapters.
- **Portable proof bundles** that can be verified without the producer database or network service.
- **OTel-style interoperability** through the dependency-free `habitat.otel` bridge.
- **CI verification** for checked-in proof artifacts.
- **Supervision signals** when recorded behavior needs attention.

## What Habitat proves — and does not

Habitat can establish that a matching action was recorded, that the ledger is internally consistent, that a claim matches an exact run when a run ID is supplied, or that an explicit evidence adapter returned an expected result.

Habitat does **not** establish that an agent's private reasoning was correct, that a compromised host is trustworthy, or that a local database is independently anchored cryptographic truth.

These boundaries are part of the product contract, not footnotes.

## Quick start

Requirements:

- Python 3.10+
- SQLite (included with Python)
- No third-party runtime dependencies

Install Habitat, then initialize a local database:

```bash
pip install habitat            # add: pip install 'habitat[signing]' for Ed25519 signing
# From a source checkout instead: pip install -e .

habitat init --config examples/simple.yaml
habitat demo                   # records one sample action (run-42) — labelled sample data
```

### Generate portable proof

`habitat demo` records a sample `run_job` action with run ID `run-42`, so the
command below succeeds on a fresh database. (`habitat seed` is an alias.)

```bash
habitat prove \
  --run-id run-42 \
  --claim "deployed v1.2.3 to production" \
  -o proof.json --card

python tools/verify_proof.py proof.json   # → VALID, exit 0
```

Notes:

- `--card` writes `proof.md` alongside `proof.json` and names the proof file
  that was actually written. Without `-o`, `--card` defaults to `proof.json`.
- If `prove` is rejected (for example, an unknown `--run-id`), it prints an
  explanation, what would change the verdict, and the next action — it does
  not just print a reason code.
- The proof created from `habitat demo` is sample data: it shows the claim
  matches evidence in the local ledger. It does not prove the claim is true
  in the world.

For an executable end-to-end example:

```bash
python examples/prove_run.py
```

Portable proof can be checked on another machine without access to the producer's database or network service.

## OpenTelemetry interoperability

Habitat does not require a new tracing protocol.

```text
Agent / framework
      ↓
OpenTelemetry
      ↓
Habitat bridge
      ↓
Trusted ledger → Verification → Portable proof
```

See [OTEL.md](OTEL.md), [ADOPTION.md](ADOPTION.md), and [examples/otel_bridge.py](examples/otel_bridge.py).

## Verification

The repository includes automated tests and an independent proof verifier. GitHub Actions can verify a checked-in `proof.json` without installing Habitat's runtime dependencies.

Read [VERIFY_PROOF.md](VERIFY_PROOF.md) and [PROOF.md](PROOF.md) for the verification contract.

## Documentation

- [PROJECT.md](PROJECT.md) — project scope and operating model
- [PROTOCOL.md](PROTOCOL.md) — event and protocol contract
- [ARCHITECTURE.md](ARCHITECTURE.md) — system boundaries
- [SECURITY.md](SECURITY.md) — threat model and security principles
- [PROOF.md](PROOF.md) — proof model
- [VERIFY_PROOF.md](VERIFY_PROOF.md) — independent verification
- [ADOPTION.md](ADOPTION.md) — integration path
- [MONETIZATION.md](MONETIZATION.md) — monetization hypotheses (no traction claimed)
- [RELEASE_VERDICT.md](RELEASE_VERDICT.md) — release verdict: library ready, service not ready (73/100)
- [INDEPENDENT_REVIEW.md](INDEPENDENT_REVIEW.md) — five-perspective independent review
- [PRODUCT_IDENTITY.md](PRODUCT_IDENTITY.md) · [COMPETITIVE_BENCHMARK.md](COMPETITIVE_BENCHMARK.md) · [UX_AUDIT.md](UX_AUDIT.md) · [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) — Phase 1–4 audit set
- [CHANGELOG.md](CHANGELOG.md) — release history

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Security

Please report suspected vulnerabilities privately. Never include real credentials, tokens, private agent transcripts or sensitive evidence in public issues.

## License

Habitat is released under the MIT License. See [LICENSE](LICENSE).
