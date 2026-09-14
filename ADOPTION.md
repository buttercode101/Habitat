# Habitat adoption wedge

Habitat should be adopted **beside** an existing agent stack, not as a replacement for it.

## The one-line value proposition

> Keep your agent framework and observability stack. Add Habitat when a claim needs evidence that another system can independently inspect.

## Where Habitat sits

```text
Agent / framework
      |
      v
OpenTelemetry / existing telemetry
      |
      v
Habitat accountability bridge
      |
      +--> evidence + trusted actions
      |
      v
claim verification
      |
      v
portable proof
      |
      v
independent verifier
```

The OTel bridge is intentionally dependency-free and projects only accountability-relevant operations. It reuses an existing trace ID as the Habitat run ID rather than creating a competing tracing identity. See `OTEL.md` and `examples/otel_bridge.py`.

## The first integration should be tiny

A developer should not have to replace an SDK, framework, model provider, or observability backend.

1. Keep the existing agent stack.
2. Export the existing trace/event data you already have.
3. Feed accountability-relevant spans through `habitat.otel.events_from_spans(...)`.
4. Record the resulting trusted events in Habitat.
5. Verify claims against Habitat evidence.
6. Export a proof bundle when another system needs to inspect the result.

## Proof exchange

The receiver does not need the producer's database or Habitat runtime. A producer can send the exported JSON proof bundle to another service, team, or agent; the receiver can independently validate its digest and claim/ledger relationships with:

```bash
python examples/proof_exchange.py proof.json
```

This is deliberately a file-level exchange primitive first. It avoids inventing a hosted proof network before the portable proof contract has real adoption.

## Why this is different

Observability products are primarily optimized to answer:

- What happened?
- Where did the run fail?
- How much did it cost?
- Which prompt/model/tool was involved?

Habitat adds a narrower question:

- **What evidence supports the claim that this action happened, under this run and identity, and does that evidence satisfy the configured verification policy?**

Habitat is therefore complementary to tools such as LangSmith, Langfuse, Arize Phoenix, AgentOps, and other OTel-compatible observability systems rather than trying to out-feature them.

## Adoption rule

Do not add framework-specific integrations until the generic protocol path is strong enough that an integration is only a convenience wrapper.

Prefer:

```text
standard telemetry -> Habitat protocol -> proof
```

over:

```text
Habitat plugin for every framework
```

This keeps the core small and makes each new framework an acquisition channel rather than a permanent architectural dependency.

## What not to claim

A valid Habitat proof is not automatically proof that an external-world claim is true. It establishes the integrity and consistency of the evidence Habitat received and the verification rules applied to it. External truth, host compromise, and key custody remain explicit trust boundaries.
