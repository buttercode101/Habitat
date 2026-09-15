# Habitat real-work proofs

These artifacts record real work performed in other projects and verified by Habitat. They are intentionally conservative: a valid Habitat proof is not automatically a deployment attestation, publisher attestation, or statement of real-world truth.

## Current proof set

| Project | Real change | Habitat | External execution evidence |
|---|---|---:|---|
| Greenlight-k53 | K53 database cache refresh with offline fallback | VERIFIED | GitHub Actions: success |
| Rosendaltown | Correct category/content image mapping and homepage imagery | VERIFIED | Vercel: success |
| Diketo | Low-end performance soft limits | VERIFIED | Vercel: success |
| SoloBid-v2 | Invoice-native DueToday coverage and UI lanes | VERIFIED | Not exposed for the historical SHA |

## Assurance model

- **Habitat verified** means the claim matched Habitat's trusted ledger and the portable proof passed its integrity and consistency checks.
- **External execution evidence** is reported only when an actual external status was observed for the referenced work.
- **Publisher trust** is a separate question: a valid signature or proof does not, by itself, establish that the publisher is authorized or trustworthy.
- **External truth** is also separate: evidence recorded by Habitat cannot prove facts that were never observed or independently attested.

## Independent verification

Every JSON artifact can be checked without installing Habitat:

```bash
python tools/verify_proof.py proofs/<proof-file>.json
```

A result of `VALID` means the proof bundle is structurally valid, internally consistent, and content-integrity checked according to the verifier. Read the corresponding Markdown card for the evidence boundary of the individual claim.

## Evidence discipline

Do not backfill CI, deployment, runtime, or production claims into an older proof merely because a related status exists elsewhere. Create a new proof bound to the actual execution when stronger evidence becomes available.
