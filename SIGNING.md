# Proof signing

Habitat proof bundles can optionally be authenticated with **Ed25519**. Signing is deliberately outside the core runtime so normal local deployments keep zero third-party runtime dependencies.

## Install

```bash
pip install 'habitat[signing]'
```

## Model

```text
claim + evidence + ledger result
              ↓
        canonical JSON
              ↓
          Ed25519
              ↓
       signed proof.json
```

The signature authenticates the proof bundle bytes against the embedded public key. It does **not** prove that the underlying claim is true, that the evidence came from an honest source, or that the public key belongs to a particular organization.

### Key handling

Generate keys with the signing library/API and keep the private key outside the repository. Treat it like any other signing credential. The public key may be distributed with the proof.

### Verification

A verifier checks the Ed25519 signature over the proof bundle with the `signature` field removed. A modified claim, evidence item, ledger result, or digest causes verification to fail.

The embedded `key_id` is an identifier only. It is not a trust anchor. Production systems should map trusted key IDs to an independently configured key registry or trust policy.

## Threat boundary

Habitat supports three distinct properties:

1. **Evidence:** what Habitat observed.
2. **Integrity:** whether the exported proof was modified after signing and whether Habitat's local action ledger is intact.
3. **Authenticity:** whether the proof was signed by the holder of the corresponding private key.

None of these alone proves external reality. That distinction is intentional.
