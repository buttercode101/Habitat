# Habitat

**A minimal, self-observing home for autonomous agents.**

Habitat is a local-first runtime and supervision layer. It keeps structured state, records actions, detects high-signal anomalies, and renders a human-readable supervision surface.

## Current project control

Before starting material work, read these in order:

1. **`STATUS.md`** — current verified state and exact restart point.
2. **`PROJECT_MAP.md`** — complete product/history map, including the separation between Habitat and the later Forge/Truth Layer discovery.
3. **`DECISIONS.md`** — durable decisions and unresolved questions.
4. **`ROADMAP.md`** — current work control and gates.
5. **`WORK_HISTORY.md`** — phase-based reconstruction of how the project evolved.
6. **`PROJECT_STATE.md`** — current verified state snapshot.
7. **`HANDOFF.md`** — restart and material-change procedure.

The repository is the source of truth for implementation. These control documents are the source of truth for project context and decisions. When they disagree, inspect the implementation and reconcile the documents rather than guessing.

## Core principles
- Habitat first
- Gentle by default
- Model is swappable
- Supervision is native
- Minimal surface area
- Progressive: supervise existing crews or run jobs inside Habitat

## What Habitat is
1. Thin runtime primitives for jobs, state, actions, signals and recovery hooks.
2. A native supervision surface generated from Habitat state.
3. A closed loop: agent/job runs → Habitat records truth → signals surface exceptions → human intervenes when needed.

## What Habitat is not
- Not a multi-agent orchestration framework
- Not a heavy tracing platform
- Not a visual agent builder
- Not a replacement for LangGraph, CrewAI, AgentScope, etc.

## Early success metrics
- A human understands crew health in <10 seconds.
- Silent failures become visible.
- Model switching is configuration-only.
- Adding a habitat takes minutes, not hours.

## Anti-drift rule

> **Never make the project look more complete than it actually is.**

No fake functionality, metrics, verification, security claims, or confidence. If something is unverified, say so and record it as unknown.
