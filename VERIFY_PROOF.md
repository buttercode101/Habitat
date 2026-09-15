# Verify a Habitat proof bundle

Habitat proof bundles can be checked without a Habitat database, server, or Python package installation.

## Zero-install verification

Copy `tools/verify_proof.py` and the proof JSON to the consumer machine, then run:

```bash
python tools/verify_proof.py proof.json
```

The verifier uses only Python's standard library. Exit code `0` means the bundle passed structural, content-integrity, and internal-consistency checks; a non-zero exit code means it failed or could not be read.

The result includes explicit assurance levels so consumers do not collapse integrity, authenticity, trust, and truth into one boolean:

- `structural_validity`: the bundle has the required supported structure;
- `content_integrity`: the content SHA-256 matches the unsigned proof contents;
- `internal_consistency`: claim, evidence, action, run, and ledger relationships are coherent;
- `signature`: `absent` or `present-unverified` in the zero-install verifier;
- `publisher_trust`: `not-assessed` unless a consumer applies its own trusted-key policy;
- `external_truth`: always `not-established` by the proof verifier alone.

## Package-based verification

If Habitat is already installed, the same dependency-free verification is available through its Python API:

```python
from habitat.proof_verify import verify_file

result = verify_file("proof.json")
assert result["valid"]
print(result["assurance"])
```

For cryptographic signature verification and key trust, install the optional signing dependency and use `habitat.proof_sign.verify_signed_proof` plus an explicit `TrustRegistry`. A valid signature proves possession of the signing key; a trusted key additionally requires an independently configured trust relationship.

## What is checked

The standalone verifier checks:

- the proof content SHA-256 digest;
- required proof structure and proof version;
- claim-to-ledger habitat, job, and run correlation;
- that a claim's evidence action exists in the bundled ledger;
- evidence action/status/run consistency with the claim;
- ledger integrity state recorded in the bundle;
- that a `verified` verdict is not paired with a failed ledger-integrity state.

If an optional Ed25519 signature is present, its fields are structurally checked and reported as `present-unverified`. The zero-install verifier deliberately does not pretend to perform cryptography it does not ship.

## Signed proof export

The CLI can sign an exported proof without putting a private key on the command line:

```bash
export HABITAT_SIGNING_KEY='<base64 Ed25519 private key>'
habitat proof CLAIM_ID --reverify \
  --signing-key-env HABITAT_SIGNING_KEY \
  --key-id production-agent-key \
  --agent-id agent-01 \
  --output proof.json
```

The proof content digest excludes the optional `signature` field, so adding a signature does not rewrite the underlying proof content. The Ed25519 signature covers the complete unsigned proof bundle, including its content digest.

## Protocol boundary

`valid: true` means the bundle is structurally valid, internally consistent, and its content digest matches. It does **not** mean that the publisher is trusted, that a signature is cryptographically verified by the zero-install verifier, or that every statement in the bundle is independently true.
