# Habitat — Independent Review (Final Phase)

**Date:** 2026-11-08
**Repo:** `buttercode101/Habitat` @ `2194d58`
**Method:** Five independent perspectives, each judged against observed evidence only (code, tests, live site, docs).
Where a perspective could not verify something, it says so. Scores are judgement, not measurement.

**QA baseline for all five:** `python3.13 -m pytest -q` → **116 passed**; `PYTHONPATH=. python3.13 examples/prove_run.py` →
**Standalone verification: VALID**; fresh-DB smoke `init → demo → prove --run-id run-42 → tools/verify_proof.py`
→ **VALID, exit 0 at every step** (2026-11-08, this phase).

---

## Perspective 1 — The Developer Adopter (DX)

**Verdict: Adopt as a library; first-run path is fixed, install story still soft.**

- *What works:* Zero runtime deps, SQLite included with Python, one-command first proof
  (`habitat demo` seeds `run-42`, then `habitat prove` succeeds on a fresh DB — verified this phase).
  `tools/verify_proof.py` is genuinely copy-anywhere: stdlib-only, exit 0/1, single file.
  Rejected proofs explain themselves: reason + what would change the verdict + next action (`habitat/verdicts.py`).
- *What hurts:* Install is still the softest step (`UX_AUDIT.md` §1.1) — README now shows `pip install habitat`,
  but examples still need `PYTHONPATH=.` or an installed package when run as scripts, and the changelog is sparse
  (one dated entry). A developer evaluating in an afternoon will hit docs quality before code quality.
- *Adoption call:* Fine for a sidecar evidence layer beside LangGraph/OTel. Not fine as a platform purchase —
  there is no platform.

## Perspective 2 — The Security Reviewer

**Verdict: Sound threat model for what it claims; not a security product.**

- *What works:* HMAC-signed ingest by default, PBKDF2 agent secrets with legacy auto-upgrade, constant-time
  comparison, SSRF-hardened HTTP adapter (HTTPS-only, DNS pre-resolution, private-IP rejection), strict JSON
  (non-finite numbers rejected), proof caps (16 MiB / 10,000 actions), timezone-aware timestamps,
  hash-chained ledger, six-level assurance model that refuses to upgrade `inconclusive`.
- *What hurts:* A compromised host is explicitly out of scope (`PRODUCT_IDENTITY.md` §1.4) — correct, but it means
  Habitat proves *internal consistency*, not *truth*. No key-management runbook, no production deployment to
  review, Ed25519 signing optional and off by default in the demo flow (`signature: absent` in the smoke proof).
- *Security call:* Trustworthy *as designed* for local accountability. Do not deploy it as a public evidence
  service without the runbook, TLS, and network restriction that `VERCEL.md` describes as manual steps.

## Perspective 3 — The Platform / DevOps Operator

**Verdict: Easy to run locally, not yet operable as a service.**

- *What works:* `habitat serve` binds `127.0.0.1:8787` by default (safe default), SQLite with WAL + foreign keys,
  `doctor`/`backup`/`restore` exist, Vercel proxy enforces HTTPS + 10s timeout and keeps the bearer token
  server-side, dashboard degrades to disclosed demo data rather than fabricating status.
- *What hurts:* No Dockerfile, no IaC, no persistent-host deployment — `RELEASE_ACCEPTANCE_REPORT.md` (73/100)
  names this as the core reason for NOT READY as a production service. SQLite on an ephemeral filesystem would
  silently lose the ledger if someone deployed naively. No uptime/SLI story, because there is no service.
- *Operator call:* Runs happily on a laptop or a small VPS you manage yourself. Budget and staff it as a
  self-hosted tool, not as a managed service — because it isn't one.

## Perspective 4 — The Skeptical Buyer / Auditor

**Verdict: The honesty is the product. Buy the evidence discipline, not a promise.**

- *What works:* Anti-drift rule D-014 is enforced in practice: the public Evidence archive was narrowed to 2
  directly reconciled artifacts after stale/mislabeled proofs were found (historical paths quarantined, not
  relabeled); the Rosendäl card correctly shows `UNVERIFIED`; demo data is labelled `sample: true` inside the
  proof payload itself; `external_truth` is always `not-established` by the verifier alone.
- *What hurts:* That same honesty means there is almost nothing to buy: no hosted tier, no SLA, no references,
  no traction (0 stars/forks, no customers — `MONETIZATION.md`). An auditor can verify a proof bundle today for
  free and in one command; there is no paid assurance wrapper around it.
- *Buyer call:* Worth evaluating for handover/release/diligence evidence flows *because* it doesn't oversell.
  Anyone selling you "verified truth" from this tool is misusing it — the tool itself tells you so on every card.

## Perspective 5 — The Maintainer / Open-Source Steward

**Verdict: Clean, small, and honestly scoped. Bus-factor and discoverability are the risks.**

- *What works:* 2,898 LOC across 27 modules, 27 test files (116 tests green this phase), MIT license, CI across
  Python 3.10–3.13, decisions recorded (`DECISIONS.md` D-001–D-014), hypotheses kept separate from evidence
  (`PRODUCT_IDENTITY.md` §4), quarantined proofs kept as evidence of past error rather than deleted.
- *What hurts:* 1 contributor, 0 stars/forks, sparse changelog, no release cadence evidence, and the Truth Layer
  experiments (H1–H5) designed but **none executed**. The project is one person deep and pre-adoption; if that
  person stops, the honest artifact remains but the project doesn't grow.
- *Steward call:* A good citizen OSS tool. The highest-leverage maintenance act now is executing one H-experiment
  and publishing the result — especially a negative one — rather than adding features.

---

## Convergence

| Question | All five perspectives agree |
|---|---|
| Ship as library + CLI + standalone verifier? | **Yes** — proven, tested, honest (116/116, VALID, fresh-DB smoke) |
| Ship as a production evidence *service*? | **No** — no deployment, no runbook, no auth, no SLA (73/100) |
| Is the demo surface labelled as demo? | **Yes** — in UI copy, in `proof.md`, and inside `proof.json` (`sample: true`) |
| Is there traction / a business? | **No** — and the project correctly does not claim any (`MONETIZATION.md`) |
| Biggest next step | Run one H-experiment (cold takeover or buyer test) and publish the outcome, positive or negative |

**One-line consensus:** Habitat is a small, well-tested, unusually honest evidence *tool* that is not yet — and
should not be sold as — an evidence *service*.
