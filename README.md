# Habitat

**A local-first supervision and evidence runtime for autonomous agents.**

> Agents can tell you what they did. Habitat helps you verify whether the record supports the claim.

Habitat is deliberately smaller than a full observability or orchestration platform. It records trusted actions locally, accepts authenticated structured events, correlates work with run IDs, verifies claims against a tamper-evident action ledger or explicit external evidence, and raises supervision signals when behavior needs attention.

## Why Habitat exists

Agent observability is becoming crowded: platforms such as LangSmith and Langfuse focus on tracing, monitoring, evaluation, cost, and production debugging. Habitat starts one layer closer to accountability: **when an agent says “I did X,” what evidence does the system actually have for that statement?**

That distinction is intentional. Habitat is not trying to replace tracing, evals, or orchestration. It can sit underneath or beside those systems as a small evidence and supervision layer, especially where local-first operation and deterministic verification matter.

## Interoperability first

Habitat does not invent another tracing protocol. `habitat.otel` provides a dependency-free bridge for OTel-style GenAI spans, using an existing `trace_id` as the Habitat `run_id` and projecting only accountability-relevant operations. See `OTEL.md` and `examples/otel_bridge.py`.

```text
Agent / framework
      ↓
OpenTelemetry
      ↓
Habitat bridge
      ↓
Trusted ledger → Verification → Portable proof
```

## Core model

```text
Agent → Event → Habitat ledger → Integrity → Verification → Signal → Human
                         ↓
                       SQLite
```

## What Habitat proves — and what it does not

Habitat can establish that a matching action was recorded, that the action ledger is internally consistent, that a claim matches an exact run when a run ID is supplied, or that an explicit external evidence adapter returned the expected result.

Habitat does **not** prove that an agent's private reasoning was correct, that a compromised host is trustworthy, or that a local database has independently anchored cryptographic truth. Those boundaries are deliberate and documented in `SECURITY.md`.

## Requirements

- Python 3.10+
- No third-party runtime dependencies
- SQLite (included with Python)

## Development

```bash
python -m pytest -q
```

See `PROJECT.md`, `PROTOCOL.md`, `ARCHITECTURE.md`, `SECURITY.md`, and `PROOF.md` for the design and operating boundaries.

## License

MIT.
