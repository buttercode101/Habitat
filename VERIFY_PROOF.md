# Verify a Habitat proof bundle

Habitat proof bundles can be checked without a Habitat database, server, or Python package installation.

## Zero-install verification

Copy `tools/verify_proof.py` and the proof JSON to the consumer machine, then run:

```bash
python tools/verify_proof.py proof.json
```

The verifier uses only Python's standard library. Exit code `0` means the bundle passed verification; a non-zero exit code means it failed or could not be read.

## Package-based verification

If Habitat is already installed, the same verification is available through its Python API:

```python
from habitat.proof_verify import verify_file

result = verify_file("proof.json")
assert result["valid"]
print(result["verdict"])
```

## What is checked

The standalone verifier checks:

- the proof content SHA-256 digest;
- required proof structure and proof version;
- claim-to-ledger habitat, job, and run correlation;
- that a claim's evidence action exists in the bundled ledger;
- evidence action/status/run consistency with the claim;
- ledger integrity state recorded in the bundle;
- that a `verified` verdict is not paired with a failed ledger-integrity state.

The standalone verifier intentionally does **not** establish external-world truth or publisher identity. A proof file is an integrity-verifiable evidence package, not by itself a cryptographic signature. Authenticity should be established by the transport, repository, or signing system used by the consuming application.

## Protocol boundary

`valid: true` means the bundle is internally consistent and its content digest matches. It does not mean that every statement in the bundle is independently true.
