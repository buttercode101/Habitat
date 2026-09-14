# OpenTelemetry bridge

Habitat is **not** an observability replacement. OpenTelemetry already provides the common telemetry language for traces, metrics, logs, and GenAI operations, including `invoke_agent`, `invoke_workflow`, and model/tool telemetry. Habitat uses that ecosystem as an input boundary and adds a different question: **does the evidence support the agent's claim?**

## Design

```text
Agent / framework
       |
       v
OpenTelemetry spans/events
       |
       v
habitat.otel.events_from_spans()
       |
       v
Habitat events -> trusted action ledger -> verification -> proof bundle
```

The bridge deliberately projects only accountability-relevant operations. Ordinary model/debug spans remain in the user's existing observability system. The OTel `trace_id` becomes Habitat's `run_id`, preserving correlation without duplicating an entire trace database.

## Why this boundary

OpenTelemetry's GenAI conventions already standardize agent/model/tool telemetry. Habitat should not fork that work. Instead, Habitat adds a local, evidence-oriented layer above it.

This keeps Habitat small, dependency-free, and compatible with agents that already emit OTel-style telemetry.

## Important limitation

An OTel span is **telemetry, not proof**. A converted event means Habitat received an observation. A `VERIFIED` claim still requires Habitat's own trusted ledger and verification rules. If the ledger integrity check fails, the result remains `INCONCLUSIVE`.
