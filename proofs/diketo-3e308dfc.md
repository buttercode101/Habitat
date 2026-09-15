# Habitat Proof — Diketo

**Claim:** Shipped Diketo change: added low-end performance soft limits for the game.

| Check | Result |
|---|---|
| Habitat claim | `VERIFIED` |
| Source | `habitat_trusted_ledger` |
| Action | `diketo-commit-3e308dfce343` |
| Run binding | `3e308dfce343e137a08b11d0810884d3d27f75d9` |
| Ledger | `intact` |
| External execution | **Vercel: success** |
| Proof digest | `33ef95ebac81b630344a725b25c4ea3d528bd5094b264bbfb8165570c8f5064b` |

## Verify independently

```bash
python tools/verify_proof.py proof.json
# → VALID
```

## Evidence boundary

This proof establishes the recorded commit claim, proof integrity, and internal consistency. The referenced commit also has an external Vercel success status. Habitat does **not** infer publisher trust or real-world truth merely from a valid proof bundle; those remain separate assurance dimensions.
