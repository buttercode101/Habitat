# Habitat — Project State

**State record:** append-oriented restart snapshot  
**Recorded:** 2026-09-25  
**Repository:** `buttercode101/Habitat`  
**Branch:** `main`  
**Current commit:** `555490d13b1045ef86d517a77b6c07a26681a4ad`

## Verified facts

- The repository is public, unarchived, and `main` is the default branch.
- The live site is `https://habitat-za.vercel.app`.
- The corrected Evidence route was browser-verified after the reconciliation changes.
- The public proof manifest contains exactly two reconciled artifacts: Greenlight-K53 and Diketo.
- Both listed proof routes resolve successfully.
- The stale `22 proofs / 8 projects` presentation was removed.
- Landing, dashboard, proof inspection, tamper simulation, reset, JSON download, responsive behavior, and the public GitHub CTA were browser-verified.
- The dashboard discloses that the live backend is unavailable and uses checked-in demo proof instead of pretending the data is live.
- GitHub Actions on the current commit completed successfully for Python 3.10, 3.11, 3.12, 3.13, and dependency audit.
- The current commit fixes a test expectation so it matches the verifier's explicit tamper error.

## Assurance boundary

Verified here means repository or browser evidence exists for the stated behavior. It does not mean:
- external-world truth;
- publisher trust beyond the documented trust model;
- a live Hermes installation has been exercised;
- a production backend is running;
- customers or revenue exist;
- the Truth Layer hypothesis is validated.

## Current product boundary

Habitat remains the implemented product. Forge / Project Truth Layer remains a hypothesis and has not been promoted into the shipped product.

## Open validation work

The following are experiments, not completed facts:
1. cold takeover;
2. truth decay;
3. agent switching;
4. broken-project rescue;
5. buyer/economic-value test.

No result should be recorded as positive or negative until the experiment has been executed and its evidence captured.

## Restart rule

A future agent should read `STATUS.md`, `PROJECT_MAP.md`, `DECISIONS.md`, `ROADMAP.md`, this file, and `HANDOFF.md` before material work. Treat unknowns as unknowns and verify implementation before changing direction.
