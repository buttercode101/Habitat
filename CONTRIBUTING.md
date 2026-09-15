# Contributing to Habitat

Thank you for your interest in Habitat. This document explains how to develop, test, and contribute changes.

## Design principles

Please keep these constraints in mind:

- **Local-first and minimal dependencies** — the core runtime uses only the Python standard library + SQLite. The only optional dependency is `cryptography` (for Ed25519 proof signing).
- **Honest security boundaries** — document what Habitat does *not* prove. Do not over-claim.
- **Portable proof** — a proof bundle must remain independently verifiable without the producer's database or network service.
- **Protocol over plugins** — prefer a clean event/proof protocol that any agent stack can feed, rather than deep framework-specific integrations.
- **Small surface area** — new features should earn their place.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -e ".[signing]"
pip install pytest
```

## Running tests

```bash
# Core suite (no extra deps required)
python -m pytest -q

# Signing / trust tests (requires the optional extra)
python -m pytest -q tests/test_proof_sign.py tests/test_trust.py
```

CI runs the full matrix on Python 3.10–3.13 and includes a dependency audit.

## Useful local commands

```bash
# Initialize a demo habitat
habitat init --config examples/simple.yaml

# Run once
habitat run

# Continuous supervision loop
habitat run --watch --interval 5

# Generate the HTML supervision surface
habitat generate -o dashboard.html

# Doctor / health checks
habitat doctor
```

## Pull request checklist

- [ ] Tests cover new verification, security, ledger, or protocol behavior.
- [ ] `CHANGELOG.md` updated under an `## Unreleased` (or next version) heading.
- [ ] Documentation updated when behavior or public contracts change.
- [ ] No secrets or agent credentials committed.
- [ ] Code stays readable and avoids unnecessary abstraction.

## Security-sensitive changes

Changes that affect:

- event signature verification
- action ledger integrity
- claim verification logic
- proof format or the standalone verifier
- agent authentication / permissions
- HTTP evidence adapters

require careful review and strong regression tests. Prefer explicit, conservative defaults.

## Code of conduct

Be respectful. Focus on technical merit and clear communication.
