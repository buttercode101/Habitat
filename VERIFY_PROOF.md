# Verify a Habitat proof bundle

Habitat proof bundles can be checked without a Habitat database or server.

```python
from habitat.proof_verify import verify_file

result = verify_file("proof.json")
assert result["valid"]
print(result["verdict"])
```

The standalone verifier checks:

- the proof content SHA-256 digest;
- required proof structure;
- ledger integrity state recorded in the bundle;
- that a `verified` verdict is not paired with a failed ledger-integrity state.

It intentionally does **not** establish external-world truth or publisher identity. A proof file is an integrity-verifiable evidence package, not a cryptographic signature. Authenticity should be established by the transport, repository, or signing system used by the consuming application.

## Protocol boundary

`valid: true` means the bundle is internally consistent and its content digest matches. It does not mean that every statement in the bundle is independently true.
