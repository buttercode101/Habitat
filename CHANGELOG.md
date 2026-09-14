# Changelog

## 1.2.0

- Added optional Ed25519 signing for portable proof bundles.
- Added an explicit trust registry with key expiry and revocation semantics.
- Added deterministic evidence policies for source/action/status, run binding, freshness, and required detail keys.
- Added GitHub Actions coverage across Python 3.10–3.13 and the optional signing stack.

## 1.0.1

- Added a tamper-evident SHA-256 hash chain for trusted actions.
- Claim verification now refuses to treat a corrupted or incomplete action ledger as trusted.
- Added regression coverage for action-ledger tampering.
- Documented the integrity boundary and clarified that the local ledger is evidence, not independently anchored remote attestation.

## 1.0.0

- Added agent registry and least-privilege permissions.
- Added secure structured event protocol.
- Added exact run/correlation claim binding for network submissions.
- Added signal recovery lifecycle.
- Added continuous scheduling loop.
- Added typed external evidence predicates.
- Added live HTTP supervision API.
- Added doctor diagnostics.
- Added SQLite backup/restore commands.
- Hardened shell execution with argv parsing by default.
- Added release documentation, protocol specification, and security model.
- Added release-level integration and security-behavior tests.
- Switched package build backend to setuptools for reliable wheel creation.
