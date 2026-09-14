# Machine-readable verification

Habitat can expose a claim as a machine-readable verdict plus a portable proof bundle.

## HTTP API

For an existing claim:

```text
GET /v1/claims/<claim-id>/proof
```

Returns the stored verdict, ledger-integrity state, content digest, and proof bundle without changing the claim.

To re-run Habitat's deterministic verification first:

```text
GET /v1/claims/<claim-id>/verify
```

That endpoint verifies the claim, stores the resulting decision, and returns the decision plus proof.

## CLI

```bash
habitat proof <claim-id>
habitat proof <claim-id> --reverify
```

`--reverify` is the explicit mutation operation: it recalculates the claim decision before producing the proof.

## What consumers should trust

A consumer should treat `verdict=verified` as: Habitat found evidence matching its configured verification rules and its own trusted action ledger was intact at verification time.

It should **not** treat the result as a universal assertion about the outside world. External evidence quality, source authenticity, and the configured verification predicate still matter.

The `content_sha256` digest makes the proof bundle content-addressable for downstream systems. `generated_at` is intentionally excluded from the digest so regenerating the same observed evidence can produce the same content digest.
