# Habitat

**A minimal, self-observing home for autonomous agents.**

Habitat is a local-first runtime and supervision layer. It keeps structured state, records actions, detects high-signal anomalies, and renders a human-readable supervision surface.

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
