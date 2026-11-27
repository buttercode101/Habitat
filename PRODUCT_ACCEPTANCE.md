# Product acceptance — 27 November 2026

This is the current acceptance record for the local-first CLI, proof workflow and web interface. Older release verdicts remain historical snapshots.

## Verified product workflows

| Check | Result |
|---|---|
| Python test suite | 107 passed, 5 skipped |
| Web unit tests | 3 passed |
| Playwright product workflows | 5 passed |
| Production Next.js build | Passed |
| npm audit (high severity threshold) | 0 vulnerabilities |
| Live production browser | 4 routes × 8 viewport widths = 32 checks; no horizontal overflow |
| Proof demo | digest match, tamper mismatch, reset and JSON download verified |
| Local quickstart | API/UI commands copied correctly; no placeholder token required for loopback |
| Live local API workflow | seeded claim loaded, verifier returned verified, action ledger intact, proof JSON downloaded |
| Sample-data boundary | demo claims visibly labelled SAMPLE; claim inspector warns sample evidence is not live activity |

The web commit with the local dashboard and safe proof download was merged to main and deployed to the Habitat Vercel project. Live site: https://habitat-za.vercel.app/

## What is actually delivered

- Local Python CLI for initializing a database, recording actions, correlating claims, exporting proofs and verifying them independently.
- Local loopback API plus web dashboard for inspecting actual local claims, verifying and downloading proofs without a hosted account.
- A static public site for product information and clearly labelled proof/demo workflows.
- AgentScope can read the local Habitat database through a read-only bridge; a real fixture generated a dashboard with an intact ledger, and the source database SHA-256 remained unchanged.

## Trust and operational boundaries

- The demo workflow seeds **sample** records. It does not represent a real agent action or external deployment.
- A valid unsigned proof establishes structural validity, content integrity and internal consistency of the supplied evidence. It does not establish publisher identity or external truth.
- The public Vercel site is static and does not host a persistent Habitat database or live evidence API.
- The API should be run locally on loopback unless the operator separately configures a secured deployment, authentication and key management.

## Remaining work before a hosted evidence service

- Persistent service hosting and durable database operations.
- Production authentication/authorization and key-management runbook.
- A real external agent integration run, not just the seeded sample workflow and local bridge fixture.
- Physical-device acceptance; no Android wrapper or installable offline PWA is currently delivered.

The current product is ready as a local-first CLI, standalone verifier and local web workflow. It is **not** certified as a hosted production evidence service.
