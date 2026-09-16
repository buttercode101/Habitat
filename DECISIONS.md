# Habitat — Decision Ledger

Decisions below are the durable interpretation of the project. A future agent should not reopen a settled decision without new evidence.

| ID | Decision | Status | Reason / evidence |
|---|---|---|---|
| D-001 | Keep Habitat local-first and small | Active | Core product definition; avoids becoming a hosted control plane. |
| D-002 | Do not replace existing observability/orchestration stacks | Active | OTel/LangSmith/Langfuse/Phoenix/AgentOps and agent frameworks already solve broader tracing/orchestration jobs. |
| D-003 | Treat evidence and verification as the accountability boundary | Active | The product's central question is whether an agent claim is supported by evidence. |
| D-004 | Keep claim verification distinct from external-world truth | Active | Repository security/proof model explicitly states local evidence does not establish every real-world statement. |
| D-005 | Separate identity, authorization, and cryptographic trust | Active | Security model requires independent controls and lifecycle semantics. |
| D-006 | Portable proof must be independently verifiable | Active | Proof exchange is useful only if a recipient can inspect it without the producer's database/network. |
| D-007 | Signatures/trust are assurance layers, not a single boolean | Active | Current verifier distinguishes structural validity, integrity, consistency, signature status, publisher trust and external truth. |
| D-008 | OTel is an interoperability input, not a competing telemetry protocol | Active | Existing telemetry remains valuable; Habitat projects accountability-relevant operations. |
| D-009 | Do not claim hash chains, signatures, JSON proofs or audit trails as unique moats | Active | Competitive research shows multiple adjacent implementations. |
| D-010 | Do not rename Habitat to Forge | Active | "Forge" / "Project Forge" is already heavily used publicly and the larger Forge thesis remains unvalidated. |
| D-011 | Do not build the hypothetical Truth Layer before validation | Active | The hypothesis is promising but the handoff/continuity/verification space is crowded. |
| D-012 | Use real projects and behavioral experiments, not preference surveys, for validation | Active | The key question is whether durable evidence changes agent behavior and produces economic value. |
| D-013 | Transactional monetization is a hypothesis worth testing before seat-based SaaS | Experimental | Trust events such as verified handover/release/rescue have clearer economic consequences than generic dashboard access. |
| D-014 | Never make the project look more complete than it is | Permanent principle | No fake functionality, metrics, verification, security claims or confidence. |

## Reopening rule

A decision may be reopened when there is new evidence that materially changes its premise. Record the new evidence and the resulting decision here; do not silently overwrite history.

## Current unresolved decisions

1. Whether the evidence/proof primitives should remain the primary Habitat product or become the foundation of a broader project-truth system.
2. Whether the proposed Truth Layer is sufficiently differentiated from existing continuity, handoff, audit, provenance and verification products.
3. Which real-world experiment produces the strongest measurable signal.
4. Whether any customer will pay for a concrete verification/assurance transition.
