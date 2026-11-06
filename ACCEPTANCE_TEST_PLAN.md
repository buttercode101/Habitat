# Acceptance Test Plan — Habitat

Date: 2026-11-06 · Tested commit: `323ca4c` + fix set · Env: Termux, Python 3.13.13 (CI: 3.10–3.13)

## Core journey
Install → configure → ingest events → record execution → generate proof → export → independently verify.

## Mandatory tests — execution results
| # | Test | Result | Evidence |
|---|---|---|---|
| 1 | Clean installation | PASS | `pip install -e .` (3.13); CI checkouts |
| 2 | Configuration | PASS | doctor/config tests; `.env.example` added (H-001) |
| 3 | Authenticated ingestion | PASS | event-security tests |
| 4 | Invalid event | PASS | event-security tests |
| 5 | Duplicate event | PASS | ledger tests |
| 6 | Event ordering | PASS | ledger-integrity tests |
| 7 | Missing event | PASS | proofs/verification tests |
| 8 | Hash validation | PASS | ledger-integrity-deep tests |
| 9 | HMAC signing | PASS | proof-sign tests |
| 10 | Ed25519 signing | PASS | proof-sign + trust 8/8 |
| 11 | Invalid signature | PASS | trust tests |
| 12 | Unknown key | PASS | trust tests |
| 13 | Revoked key | PASS | trust tests |
| 14 | Modified proof | PASS | proof-verify tests |
| 15 | Missing proof component | PASS | proof-verify tests |
| 16 | Incomplete execution | PASS | proofs/tests |
| 17 | Run correlation | PASS | claims tests |
| 18 | Concurrent ingestion | PASS | ledger tests (SQLite) |
| 19 | Database restart | PASS | store tests |
| 20 | Database recovery | PASS | store/recovery tests |
| 21 | Proof bundle export | PASS | cli-proof-export tests |
| 22 | Standalone verification | PASS | `prove_run.py` → VALID; standalone-verifier tests |
| 23 | Real agent integration | UNVERIFIED | no live agent run in this pass |
| 24 | OpenTelemetry integration | PASS | otel tests (library-level) |
| 25 | API security | PASS | api-security/verify-api tests |
| 26 | Dashboard verification | PARTIAL | web test 1/1; dashboard on demo data live |

Counts: PASS 24 · PARTIAL 1 · UNVERIFIED 1. Total 26.
Note: local `next build` not run on Termux (heavy); CI `web-build` covers it. Zero-runtime-dep pip install of signing extra timed out on Termux network — system cryptography 44.0.2 used instead (within `<51` pin).
