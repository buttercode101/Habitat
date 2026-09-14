# Habitat proof bundles

Habitat can export a claim decision as a small, portable JSON proof bundle.

```python
from habitat.proof import export_proof

export_proof(store, claim_id, "claim-proof.json")
```

A proof contains:

- the claim and its final verdict;
- the run/job correlation identifiers;
- the relevant trusted actions;
- the action-ledger integrity result;
- the evidence attached to the claim; and
- a SHA-256 content digest over the observed proof contents.

## What the proof means

A `verified` proof means Habitat's verification rules accepted the claim using
its trusted local evidence and the action ledger was intact when the proof was
created. An `inconclusive` proof is intentionally not upgraded to `verified`.

The content hash makes accidental changes to an exported proof detectable. It
does **not** prove that an external system or real-world event occurred, and it
does not make the local SQLite database immutable. External anchoring or a
separate trust service can be layered on later without changing this format.

That boundary is intentional: Habitat proves what its evidence supports rather
than pretending that an internal log is automatically ground truth.
