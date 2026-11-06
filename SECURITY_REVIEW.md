# Security Review — Habitat

Date: 2026-11-06 · Commit `323ca4c` + fix set.

## Observed (verified)
- Zero runtime dependencies in core — minimal supply-chain surface.
- `pip-audit --local` green in CI; `npm audit` gate in web.yml.
- Event auth: `HABITAT_WEBHOOK_SECRET` / `HABITAT_AGENT_SECRET` server-side only; doctor checks secret presence.
- Web: `HABITAT_API_TOKEN` server-only (never `NEXT_PUBLIC_*`); production HTTPS enforced; 10s timeout; 2 MiB bounded upstream (`web/lib/habitat.ts`).
- Tamper evidence: hash chain + HMAC/Ed25519 verified by 116-test suite (signing/trust 8/8).
- Branch protection: FIXED 2026-11-06 (H-003).

## Not verified / gaps
- Unauthorised API access: api-security tests pass at library level; a live-network unauthenticated probe against a deployed backend was not possible (no backend deployed) — UNVERIFIED at network level.
- Dashboard authentication: explicitly absent (VERCEL.md). The dashboard must not be exposed as an admin surface.
- Key management: unknown/revoked-key tests pass, but production key rotation/backup procedure is undocumented — recommend a KEY_MANAGEMENT runbook before any public deployment.

## Critical honesty note
Proof bundles prove **internal consistency** (what Habitat recorded), not real-world truth. `prove_run.py` itself states: "External truth and publisher trust are not established by this card alone." Any marketing claim beyond that is unsupported.

## Secrets hygiene
- No secrets in repo; `.env.example` contains names only. No credentials in this report.
