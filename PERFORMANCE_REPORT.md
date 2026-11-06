# Performance Report — Habitat

Date: 2026-11-06 · Env: Termux, Python 3.13.13.

## Observed
- Live `https://habitat-za.vercel.app/`: HTTP 200 (cached edge, `age` ~29h — stale-cache risk, H-005).
- Full core suite: 116 tests in 10.06s (includes ledger, proof, OTEL suites).
- `prove_run.py`: completes, standalone verification VALID.
- No Lighthouse run in this pass — no scores claimed.

## Targets (not yet measured)
- Lighthouse Performance 90+ / Accessibility 95+ / Best Practices 95+ / SEO 90+; INP ≤200ms; LCP ≤2.5s; CLS ≤0.1.
- Ingestion throughput vs SQLite WAL contention: UNVERIFIED (no load test).

## Notes
- Core is stdlib-only Python + SQLite: startup and per-event cost are low by construction, but no measurement exists. Concurrent-ingestion behaviour is tested functionally, not at load.
