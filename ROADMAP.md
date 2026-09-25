# Habitat — Roadmap / Work Control

This is a decision roadmap, not a feature wishlist.

## NOW — Reconcile the baseline

- [x] Verify the current repository/control documents against implementation.
- [x] Verify the public web deployment independently.
- [x] Verify the public GitHub CTA after repository visibility changed.
- [x] Exercise the proof inspector, tamper simulation, reset and JSON download.
- [x] Identify stale/contradictory public proof-archive content.
- [x] Narrow the public Evidence surface to directly reconciled artifacts.
- [x] Narrow the public proof manifest to the same reconciled subset.
- [x] Re-verify the corrected Evidence route and manifest in production.
- [x] Confirm current CI state on the current commit.

**Exit condition:** we can state what Habitat currently does, what is verified, and what remains unknown without relying on the old conversation.

## NEXT — Establish a reproducible project-state workflow

- [x] Define the minimum project-state record needed for future Habitat work.
- [x] Make material changes update project state + decision context.
- [x] Keep history append-only where useful; never silently rewrite why a decision was made.
- [x] Establish a compact handoff/restart procedure for future agents.

**Exit condition:** a fresh agent can enter the repo and continue correctly from repository state alone.

## VALIDATE — Truth Layer hypothesis

**Status:** deliberately open. No experiment is marked complete without measured evidence recorded in the repository.

Run the five experiments in PROJECT_MAP.md: cold takeover, truth decay, agent switching, broken-project rescue, and buyer/economic-value test. Record measured outcomes. Do not convert demonstrations into product-market-fit claims.

## DECIDE — Product boundary

Choose among evidence-backed outcomes only after the validation work. No rename or major rewrite before that decision.

## BUILD — Only after the decision

Potential workstreams, only if validated: project state model, evidence freshness/staleness, handoff protocol, claim lifecycle, verification transitions, attestation/evidence packages, CLI workflows and integrations.

## Guardrails

Never add features to chase competitors, turn hypotheses into marketing claims, or optimize for feature count instead of verified outcomes.

Every material change must answer: what problem does this solve, what evidence says it exists, why Habitat owns this boundary, what should be integrated instead, how will the change be verified, and what project-state record must change.
