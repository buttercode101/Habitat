# Habitat — Agent Handoff

## Start here

1. Read `STATUS.md`.
2. Read `PROJECT_MAP.md`.
3. Read `DECISIONS.md`.
4. Read `ROADMAP.md`.
5. Read `PROJECT_STATE.md`.
6. Inspect `main` before making changes.

## Current verified position

Habitat is the implemented product. The public deployment and reconciled Evidence surface have been independently browser-verified. The repository tip is intentionally not duplicated here; verify `main` directly before acting.

The current CI matrix is green on Python 3.10–3.13 plus dependency audit.

## What not to assume

Do not assume:
- the Truth Layer hypothesis is validated;
- Hermes integration has been exercised against a real Hermes installation;
- AgentScope integration has been merged;
- the live backend is available;
- a proof establishes external-world truth;
- excluded historical proof artifacts are valid;
- Vercel deployment/build state is identical to the current Git commit unless independently verified.

## Material-change protocol

For every material change:
1. State the problem being solved.
2. Identify repository evidence for the problem.
3. Check whether existing functionality should be integrated instead of rebuilt.
4. Make the smallest justified change.
5. Run the relevant tests/checks.
6. Verify the live surface when the change affects production UI.
7. Update `PROJECT_STATE.md` and, when the interpretation changes, `DECISIONS.md`.
8. Update `STATUS.md` / `ROADMAP.md` when a gate changes.
9. Record unresolved uncertainty instead of filling it with assumptions.

## Validation protocol

Truth Layer experiments must produce measured evidence. A conversation, design discussion, or code implementation is not an experiment result.

The five planned experiments are documented in `PROJECT_MAP.md`. Keep experiment results separate from product claims.
