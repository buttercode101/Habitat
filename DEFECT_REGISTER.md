# Defect Register — Habitat

Date: 2026-11-06 · Starting commit `323ca4c` · Tested with fix set below.

## H-001 — No root `.env.example` for the Python service (P2, FIXED)
- Evidence: `habitat/__main__.py` reads `HABITAT_WEBHOOK_SECRET` / `HABITAT_AGENT_SECRET` (via `--secret-env` flags); `doctor.py` checks `HABITAT_WEBHOOK_SECRET`; `web/lib/habitat.ts` reads `HABITAT_API_URL`/`HABITAT_API_TOKEN`. Only `web/.env.example` existed.
- Fix: added root `.env.example` (names only). `.gitignore` already covers `.env`; added `!.env.example` (defensive; verified `git check-ignore` → not ignored).

## H-002 — Duplicate `web/vercel.json` (P2, FIXED)
- Root `vercel.json` (`cd web && npm ci/build`, `web/.next`) and `web/vercel.json` (`.next`) diverged in structure — two sources of truth for one deployment.
- Fix: removed `web/vercel.json`; root remains canonical (Vercel reads project-root config). Deletion is reversible from git history.

## H-003 — No branch protection on main (P2, FIXED + VERIFIED)
- Evidence: protection API → 404 before fix.
- Fix: PUT protection — strict, required contexts [`test (3.10)`, `test (3.11)`, `test (3.12)`, `test (3.13)`, `web-build`, `dependency-audit`] (names verified via check-runs for `323ca4c`), `enforce_admins=false`, force-push/deletion blocked.
- Verification: re-GET confirms all 6 contexts, strict=true (2026-11-06).

## H-004 — Dependabot watches pip only; `web/` npm deps unwatched (P3, ACCEPTED)
- `.github/workflows` runs `npm audit` in CI (web.yml), but no Dependabot PRs for npm. Extending dependabot to npm is a one-line `dependabot.yml` addition — deferred to owner choice (PR volume vs coverage). CI audit is the current gate.

## H-005 — Live page stale cache (~29h `age`) (P3, OPEN)
- `x-vercel-cache: HIT`, age ~104,645s observed 2026-11-06. Investigate Vercel cache headers / redeploy if stale demo content persists. Not a code defect in this pass.

## Accepted limitations (not defects)
- No production backend deployment (no Dockerfile/IaC) — the live site is marketing/demo by design disclosure. Deploying the SQLite service needs owner infra decision (persistent host).
- Dashboard explicitly unauthenticated (VERCEL.md). Do not add auth without owner design decision.
- 2 open Dependabot PRs (cryptography, setuptools) — routine bumps, left for owner merge policy.
