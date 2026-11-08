# Habitat — Release Verdict (Final Phase)

**Date:** 2026-11-08
**Repo:** `buttercode101/Habitat` @ `2194d58` (branch `flagship-excellence`)
**Live:** https://habitat-za.vercel.app
**Package:** `habitat 1.3.0`, MIT, Python ≥3.10, zero runtime deps (+ optional `cryptography` for Ed25519)

> Verdict first, evidence second. If a line below reads stronger than the check behind it, treat it as a defect
> and report it — that is the project's own rule (D-014).

---

## 1. Verdict

| Claim | Verdict |
|---|---|
| **As a production evidence service** (hosted backend, SLA, public deployment) | **NOT READY** — 73/100, inherited from `RELEASE_ACCEPTANCE_REPORT.md` (2026-11-06), reaffirmed this phase. No production deployment exists; the dashboard is disclosed demo data. |
| **As a pip-installable library + CLI + standalone verifier** | **READY (with honest labels)** — 116/116 tests, `prove_run.py` VALID, fresh-DB `demo → prove → verify` smoke green (2026-11-08). |
| **As a public demo / evaluation site** | **READY** — landing + proof inspector live; demo fallback is disclosed at the point of use, not buried. |

**Convergence (all phases agree):** `PRODUCT_IDENTITY.md` (Phase 1), `COMPETITIVE_BENCHMARK.md` (Phase 2),
`UX_AUDIT.md` (Phase 3), `DESIGN_SYSTEM.md` (Phase 4), `INDEPENDENT_REVIEW.md` (5 perspectives, this phase),
and `RELEASE_ACCEPTANCE_REPORT.md` (73/100) converge on the same sentence:

> *Habitat is a local-first supervision and evidence runtime for autonomous agents — a library and CLI that
> turns agent events into policy-checked claims and portable proof. It is not a hosted service, and must not
> be sold as one.*

## 2. Scorecard (inherited, reaffirmed — not re-scored upward without new evidence)

Core 16/20 · E2E 14/20 · UI/UX 11/15 · Responsive 6/10 · Arch/Data 8/10 · Security 7/10 · Perf 4/5 · A11y 4/5 · Ops 3/5 = **73/100**

New evidence this phase (below) supports the library/CLI half; it does not move the service score, because the
service-side gaps (deployment, runbook, auth, real-agent integration) are unchanged.

## 3. QA evidence — 2026-11-08 (this phase, commit `2194d58`)

| Check | Command | Result |
|---|---|---|
| Test suite | `python3.13 -m pytest -q` | **116 passed** (1 deprecation warning, anyio/pytest — external, non-failing), exit 0 |
| Standalone proof | `PYTHONPATH=. python3.13 examples/prove_run.py` | **Standalone verification: VALID**, exit 0 |
| Fresh-DB smoke | `habitat --db <fresh> init --config examples/simple.yaml` → `demo` → `prove --run-id run-42 -o proof.json --card` → `tools/verify_proof.py proof.json` | **VALID, exit 0 at every step**; digest `e24bf317…48934`; `signature: absent`, `external_truth: not-established` (correctly scoped) |
| Demo → prove regression | (UX_AUDIT headline defect: README prove on fresh DB failed) | **Fixed and re-verified** — `habitat demo` seeds `run-42` with `sample: true`; the advertised command now succeeds |

## 4. Honest demo labelling — audited this phase

| Surface | Label present? | Evidence |
|---|---|---|
| `habitat demo` output | ✅ | `"sample": true`, `"seeded": true`, boundary sentence, *"Sample demo data recorded (not a live verification)."* |
| `proof.json` payload | ✅ | Action details carry `"sample": true`; claim/action IDs are `demo-run-42-action` — sample data is labelled *inside* the artifact, not just beside it |
| `proof.md` card | ✅ (scoped) | Status `VERIFIED` is immediately bounded: *"External truth and publisher trust are not established by this card alone."* Verifier output: `scope: bundle-integrity-and-internal-consistency`, `authenticity: not-established` |
| Web dashboard | ✅ | Discloses live-backend unavailability and demo-proof fallback (`STATUS.md`); Rosendäl card shows `UNVERIFIED` |
| README quickstart | ✅ | *"records one sample action (run-42) — labelled sample data"*; *"It does not prove the claim is true in the world."* |
| Live hero / marketing copy | ✅ | No "trusted truth" / production-service claims; hero asks *"what evidence does the system actually have?"* |

**Residual labelling risk (named, not hidden):** a `VERIFIED` proof card generated from demo data can be screenshotted
without its boundary sentence. Mitigation in place: the boundary travels inside `proof.json` (`sample: true`) and in
verifier output (`authenticity: not-established`), so any *verifiable* copy stays honest even if a screenshot doesn't.
Do not strip `sample: true` from demo actions — it is load-bearing.

## 5. What would change this verdict

| To flip… | Required evidence |
|---|---|
| Production service: READY | Persistent host deployment (Dockerfile/IaC), key-management runbook, authenticated access layer, backup/restore exercised on that host, uptime evidence |
| Score ≥ 80 | Above, plus one real-agent integration exercised end-to-end (Hermes or OTel bridge against a live system), 11-viewport + physical-device passes |
| Monetization: real | One executed H-experiment with recorded outcome (`MONETIZATION.md` §6) — especially a buyer test. Until then: hypothesis. |
| "Proxy of truth" claims | Never, by design — `external_truth` stays `not-established` by the verifier alone. This is a product boundary, not a missing feature. |

## 6. Release posture

- **Do not merge/push/deploy from this phase** — docs committed on `flagship-excellence` only, per brief.
- Next human decision (owner): persistent-host deployment *or* explicit library-only positioning. Either is
  acceptable; marketing a service that does not exist is not.
- Changelog discipline needed: `CHANGELOG.md` has one dated entry; add a `1.3.0`-era entry before any tag.
