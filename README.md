# Habitat

**A local-first supervision and evidence runtime for autonomous agents.**

Habitat records trusted agent actions, correlates work with run IDs, verifies claims against an evidence ledger or explicit external evidence, and produces portable proof that another machine can independently check.

[Live application](https://habitat-za.vercel.app) · [Quick start](#quick-start) · [Protocol](PROTOCOL.md) · [Security](SECURITY.md) · [MIT license](LICENSE)

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

Install the project according to the repository's packaging configuration, then run:

```bash
python -m pytest -q
```

### Generate portable proof

```bash
habitat prove \
  --run-id run-42 \
  --claim "deployed v1.2.3 to production" \
  -o proof.json --card

python tools/verify_proof.py proof.json
```

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
- [CHANGELOG.md](CHANGELOG.md) — release history

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Security

Please report suspected vulnerabilities privately. Never include real credentials, tokens, private agent transcripts or sensitive evidence in public issues.

## License

Habitat is released under the MIT License. See [LICENSE](LICENSE).
