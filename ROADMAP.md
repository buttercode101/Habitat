# Habitat — Roadmap / Work Control

This is a **decision roadmap**, not a feature wishlist.

## NOW — Reconcile the baseline

- [ ] Verify current repository tree against this map.
- [ ] Run/inspect the current test and CI state.
- [ ] Verify proof producer and standalone verifier agree on supported behavior.
- [ ] Verify the public web build/deployment state.
- [ ] Identify stale, duplicate, or contradictory documentation.
- [ ] Record every material discrepancy before fixing it.

**Exit condition:** we can state what Habitat currently does, what is verified, and what remains unknown without relying on the old conversation.

## NEXT — Establish a reproducible project-state workflow

- [ ] Define the minimum project-state record needed for future Habitat work.
- [ ] Make material changes update project state + decision context.
- [ ] Keep history append-only where useful; never silently rewrite why a decision was made.
- [ ] Establish a compact handoff/restart procedure for future agents.

**Exit condition:** a fresh agent can enter the repo and continue correctly from repository state alone.

## VALIDATE — Truth Layer hypothesis

Run the five experiments in `PROJECT_MAP.md`:

1. cold takeover;
2. truth decay;
3. agent switching;
4. broken-project rescue;
5. buyer/economic-value test.

Record measured outcomes. Do not convert demonstrations into claims of product-market fit.

## DECIDE — Product boundary

Choose among evidence-backed outcomes:

- Habitat remains a focused accountability/proof runtime;
- Habitat becomes the technical foundation for a separately named Truth Layer product;
- the Truth Layer hypothesis is narrowed or rejected;
- another evidence-supported direction emerges.

No rename or major rewrite before this decision.

## BUILD — Only after the decision

Potential workstreams, only if validated:

- project state model;
- evidence provenance / freshness / staleness;
- agent handoff protocol;
- claim lifecycle;
- verification transitions;
- attestation / evidence packages;
- CLI workflows;
- integrations.

Cloud, dashboards, billing, enterprise controls and broad platform surfaces remain explicitly deferred until real usage demonstrates their necessity.

## Guardrails

### Never do merely because it sounds impressive
- add features to chase competitors;
- build a dashboard because a SaaS product usually has one;
- turn hypotheses into marketing claims;
- add proprietary protocols where standards already solve the problem;
- rename the product to fit an exciting discovery;
- optimize for feature count instead of verified outcomes.

### Every material change should answer

1. What problem does this solve?
2. What evidence says the problem exists?
3. Why does Habitat own this boundary?
4. What existing standard/product should we integrate with instead?
5. How will we verify the change?
6. What project-state or decision record must change?
