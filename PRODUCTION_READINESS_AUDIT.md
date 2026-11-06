# Production Readiness Audit — Habitat

Inspection date: 2026-11-06 · Owner: Buttercode Systems (buttercode101)
Repository: https://github.com/buttercode101/Habitat · Branch: `main`
Starting commit: `323ca4ce96fa4e20880cfa8547b6884f9aa12124` (2026-11-05)
Tested commit: `323ca4c` + uncommitted fix set (see DEFECT_REGISTER.md H-001–H-003)
Environment: Termux/Android 14, Python 3.13.13 (repo: >=3.10; CI matrix 3.10–3.13)
Live site: https://habitat-za.vercel.app

## Architecture map
- **Core (root):** Python >=3.10, **zero runtime dependencies**, stdlib + SQLite. Optional `cryptography>=50.0.1,<51` for Ed25519 signing. ~2,900 LOC across 27 modules in `habitat/` (`server.py`, `store.py`, `proof*.py`, `verify*.py`, `otel.py`, `anchor.py`, `policy*.py`). CLI: `habitat = habitat.__main__:main`.
- **Web (`web/`):** Next.js 16.3.8 + React 19.2 + TypeScript, App Router. Routes `/`, `/dashboard`, `/evidence`, `/proof-demo`, `/claims/[id]`, API proxies. Presentation edge only — durable SQLite service (`habitat serve`, port 8787) must run on a persistent host; **no Dockerfile/IaC in repo**.
- Vercel config: root `vercel.json` canonical (`cd web && npm ci/build`, `web/.next`). A duplicate `web/vercel.json` existed (removed — H-002).

## Feature inventory (verified codes)
| Feature | Status | Evidence |
|---|---|---|
| Event ingestion (authenticated) | WORKING | event-security tests pass |
| Hash/HMAC/Ed25519 signing | WORKING | proof-sign + trust tests 8/8 pass (cryptography 44.0.2 system) |
| Proof generation + standalone verify | WORKING | `examples/prove_run.py` → "Standalone verification: VALID" |
| Ledger integrity / tamper detection | WORKING | ledger-integrity-deep tests pass |
| OpenTelemetry integration | WORKING | otel tests pass |
| Dashboard | WORKING (demo data) | live site discloses fallback to checked-in demo proof; backend unavailable — **not live data** |
| Production backend deployment | NOT IMPLEMENTED | no Dockerfile/IaC; ephemeral-FS warning in docs |
| Dashboard authentication | NOT IMPLEMENTED | VERCEL.md: "This is not authentication" |

## Dependency inventory
Python: zero runtime deps; optional `cryptography` only. CI `pip-audit --local` green.
Web: Next 16.3.8 / React 19.2.0 (`web/package.json`, lockfile present). Dependabot covers pip only — `web/` npm deps unwatched (accepted risk, H-004).

## Test inventory
28 test files, **116 tests collected, 116 passed** in 10.06s (2026-11-06, Python 3.13) + signing/trust 8/8 + web 1/1.
CI: `test.yml` (3.10–3.13 matrix + pip-audit + web build), `web.yml`, `tip-and-verify.yml`, `verify-proof.yml` — all green at HEAD.

## Deployment map
GitHub `main` → `test.yml`/`web.yml` → Vercel (root vercel.json) → `habitat-za.vercel.app`.
Live 2026-11-06: HTTP 200, title "Habitat — Prove what your AI agents did"; `/dashboard` 200; `/proofs`, `/api/status` 404 (correct route `/evidence`). Live page `age` ~29h (stale cache risk noted, H-005).
Deployed==source: UNVERIFIED.

## Existing defects
See DEFECT_REGISTER.md. H-001 (P2 root .env.example) fixed. H-002 (P2 duplicate vercel.json) fixed. H-003 (P2 branch protection) fixed + verified. H-004 (P3 npm dependabot gap) accepted. H-005 (P3 stale cache) open.

## Initial acceptance score
Core 16/20 · E2E 14/20 · UI/UX 11/15 · Responsive 6/10 · Arch/Data 8/10 · Security 7/10 · Perf 4/5 · A11y 4/5 · Ops 3/5 = **73/100 — NOT READY** (no production backend; see RELEASE_ACCEPTANCE_REPORT.md).
