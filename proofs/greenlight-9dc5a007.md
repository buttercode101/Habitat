# Habitat Proof — Greenlight-k53

**Claim:** Shipped Greenlight-k53 change: refresh the K53 database cache when online while retaining offline fallback.

| Check | Result |
|---|---|
| Habitat claim | `VERIFIED` |
| Source | `habitat_trusted_ledger` |
| Action | `greenlight-commit-9dc5a0071696` |
| Run binding | `9dc5a007169689babe122ccfe673faa8b03c08c4` |
| Ledger | `intact` |
| External execution | **GitHub Actions: success** |
| Proof digest | `c28f69061fe31f5be9c64915b898429462e696c930e351cc58497c9a3592ce7a` |

## Verify independently

```bash
python tools/verify_proof.py proof.json
# → VALID
```

## Evidence boundary

This proof establishes the recorded Greenlight change, proof integrity, internal consistency, and the associated successful GitHub Actions execution recorded for the real work. Habitat still keeps publisher trust and external-world truth as separate assurance dimensions.
