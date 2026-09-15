# Habitat Proof — SoloBid-v2

**Claim:** Shipped SoloBid-v2 change: added invoice-native DueToday coverage and UI lanes.

| Check | Result |
|---|---|
| Habitat claim | `VERIFIED` |
| Source | `habitat_trusted_ledger` |
| Action | `solobid-v2-commit-5d5f169f9337` |
| Run binding | `5d5f169f93376fc1cb969fd72df44c3b5c1da246` |
| Ledger | `intact` |
| External execution for this historical commit | **No status exposed** |
| Subsequent CI hardening | `92c740e758343ade32d053cfc132d33a5859530d` |
| Proof digest | `e76d99b10070255ca4104a49735a68fba0056792881ae379a2c8e1f4970dafd8` |

## Verify independently

```bash
python tools/verify_proof.py proof.json
# → VALID
```

## Evidence boundary

This proof establishes the recorded commit claim, proof integrity, and internal consistency. It does **not** claim that the historical commit passed CI or deployed successfully because no external status was exposed for that SHA. A subsequent CI workflow hardening change has been committed separately; its execution status is not promoted into this historical proof.
