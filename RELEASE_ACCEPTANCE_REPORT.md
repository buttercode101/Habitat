# Release Acceptance Report — Habitat

Date: 2026-11-06 · Starting commit `323ca4ce96fa4e20880cfa8547b6884f9aa12124`
Tested commit: `323ca4c` + fix set (`.env.example`, `.gitignore`, removed `web/vercel.json`) + 7 docs.

## Evidence ledger
| Claim | Evidence | Confidence | Last verified |
|---|---|---|---|
| 116/116 core + 8/8 signing + 1/1 web | pytest 2026-11-06 | PROVEN | 2026-11-06 |
| Standalone proof VALID | `prove_run.py` | PROVEN | 2026-11-06 |
| Live site 200 | curl habitat-za.vercel.app | PROVEN | 2026-11-06 |
| Deployed == tested commit | no Vercel API proof | UNVERIFIED | — |
| Live backend data | dashboard discloses demo fallback | DISPROVEN (by design disclosure) | 2026-11-06 |
| Real agent integration | none | UNVERIFIED | — |
| Lighthouse targets | not run | UNVERIFIED | — |

## Scorecard
Core 16/20 · E2E 14/20 · UI/UX 11/15 · Responsive 6/10 · Arch/Data 8/10 · Security 7/10 · Perf 4/5 · A11y 4/5 · Ops 3/5 = **73/100**.

## Verdict: NOT READY (as a production evidence service) / CONDITIONALLY READY as a library + CLI + demo site
No P0/P1 in code. H-001–H-003 fixed and retested. The score is below 80 because the product's core promise — a deployable evidence backend — has no production deployment (SQLite service undeployable from repo alone; no Dockerfile/IaC), the dashboard is unauthenticated demo data, and no real-agent integration is verified. As a pip-installable library with standalone verification, it is solid and honestly documented.

## Outstanding
- Owner infra decision: deploy `habitat serve` on a persistent host (or containerise it). Without this, "production" claims remain marketing-demo only.
- Key-management runbook before any public deployment.
- H-004 npm dependabot (owner choice). H-005 stale cache investigation.
- 11-viewport + physical-device passes (BLOCKED).

## Deployment
Fix set committed on `main` and pushed 2026-11-06; CI gates enforced by branch protection. Vercel web tier is git-connected; no manual deploy performed. Removing `web/vercel.json` does not change the root build config.
