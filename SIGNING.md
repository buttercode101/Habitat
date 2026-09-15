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
          SHA-256
              ↓
          Ed25519
              ↓
       signed proof.json
```

The `content_sha256` identifies the unsigned proof contents. The optional `signature` field is excluded from that digest so the same proof can be exported unsigned or signed without changing its content identity. The Ed25519 signature covers the complete unsigned proof bundle, including `content_sha256`.

The signature authenticates the proof bundle bytes against the embedded public key. It does **not** prove that the underlying claim is true, that the evidence came from an honest source, or that the public key belongs to a particular organization.

### CLI export

Keep the private key out of shell history and command arguments. Supply it through an environment variable:

```bash
export HABITAT_SIGNING_KEY='<base64 Ed25519 private key>'
habitat proof CLAIM_ID --reverify \
  --signing-key-env HABITAT_SIGNING_KEY \
  --key-id production-agent-key \
  --agent-id agent-01 \
  --output proof.json
```

`--key-id` and `--agent-id` are metadata bindings. They become meaningful for trust only when a verifier maps the key ID and public key to an independently configured trust policy.

### Key handling

Generate keys with the signing library/API and keep the private key outside the repository. Treat it like any other signing credential. The public key may be distributed with the proof.

### Verification

A verifier checks the Ed25519 signature over the proof bundle with the `signature` field removed. A modified claim, evidence item, ledger result, or digest causes verification to fail. The dependency-free verifier intentionally reports a present signature as `present-unverified`; use the optional signing dependency when cryptographic verification is required.

The embedded `key_id` is an identifier only. It is not a trust anchor. Production systems should map trusted key IDs to an independently configured key registry or trust policy.

## Assurance boundary

Habitat keeps these properties separate:

1. **Evidence:** what Habitat observed.
2. **Integrity:** whether the exported proof content matches its digest and whether Habitat's local action ledger is intact.
3. **Cryptographic authenticity:** whether the signature verifies against the embedded public key.
4. **Publisher trust:** whether that public key is trusted for the claimed publisher/agent under an independent policy.
5. **External truth:** whether the underlying real-world statement is true.

A higher level must never be inferred merely because a lower level passed. In particular, a valid hash is not a signature, a valid signature is not authorization, and a trusted publisher is not proof of external-world truth.
