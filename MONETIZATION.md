# Habitat — Monetization (Final Phase)

**Date:** 2026-11-08
**Repo:** `buttercode101/Habitat` @ `2194d58` (local clone `~/habitat-audit`)
**Companions:** `PRODUCT_IDENTITY.md` §3–4, `COMPETITIVE_BENCHMARK.md`, `RELEASE_VERDICT.md`
**Status:** Hypothesis only. **No pricing, packaging, revenue, or traction is claimed.**

> Anti-drift rule (D-014, Permanent): *Never make the project look more complete than it actually is.*
> This file exists to keep monetization thinking honest — not to imply a business exists.

---

## 1. Evidence — what is true today

| Fact | Evidence |
|---|---|
| Package | `habitat 1.3.0`, MIT, Python ≥3.10, **zero runtime dependencies** (+ optional `cryptography` for Ed25519 signing) |
| Distribution | PyPI-intended (`pip install habitat`), plus source checkout; GitHub repo public, 1 tag `v1.3.0`, 0 stars / 0 forks / 1 contributor (extract 2026-11-08) |
| Revenue / pricing / customers | **None in repo. None claimed anywhere.** No pricing page, no billing code, no customer list. |
| Decision on record | D-013 (Experimental): *"Transactional monetization is a hypothesis worth testing before seat-based SaaS"* — candidate trust events: verified handover, production-release verification, investor technical evidence package, acquisition due-diligence, project rescue, incident reconstruction |
| Live surface | `https://habitat-za.vercel.app` — landing + demo proof inspector. **Live backend is unavailable; dashboard falls back to checked-in demo proof and discloses it.** Not a hosted product. |
| What is actually usable today | Library + CLI + standalone verifier (`tools/verify_proof.py`, stdlib-only, exit 0/1). QA 2026-11-08: 116/116 pytest, `prove_run.py` VALID, fresh-DB `demo → prove → verify` smoke green (see `RELEASE_VERDICT.md` §3). |

**There is no traction to report.** Any future version of this file that adds users, revenue, or conversion
numbers must cite a measurement (installs, CI runs, support tickets) with date and source — not an estimate.

## 2. Why dev-tool adoption, not SaaS, is the only honest first motion

1. **The product is a library.** Zero runtime deps, SQLite local-first, CLI-first (`PRODUCT_IDENTITY.md` §1.6–1.7).
   The natural first adoption step is `pip install habitat` + `habitat prove`, not signing up for a hosted seat.
2. **The wedge is interoperability, not a dashboard.** Per `COMPETITIVE_BENCHMARK.md` §1, the surviving wedge is
   *verification simplicity + interoperability + boundary honesty* beside existing observability (OTel bridge included).
   A hosted control plane would compete directly with LangSmith/Langfuse-class products — a fight the benchmark
   explicitly advises against.
3. **Seat pricing contradicts the evidence.** D-013 records that generic dashboard access has unclear economic
   value, while concrete *trust events* (handover, release, rescue, diligence) carry consequence. Charging per seat
   before any of those events is observed in the wild would be pricing a hypothesis.
4. **No hosted backend exists to sell.** `RELEASE_ACCEPTANCE_REPORT.md` (73/100) and `RELEASE_VERDICT.md`:
   NOT READY as a production evidence service. Selling access to a service that is not deployed would violate D-014.

## 3. The honest adoption funnel (what to measure, not what to claim)

| Stage | Observable signal | Current state |
|---|---|---|
| Install | PyPI downloads / `pip install habitat` | Unmeasured — instrument before claiming |
| First proof | `habitat demo → prove → tools/verify_proof.py` succeeds on fresh DB | **Proven 2026-11-08** (fresh-DB smoke, exit 0 at every step) |
| Repeat proof | Second claim/run verified in CI against a checked-in `proof.json` | Supported by design; **no observed users yet** |
| Interop | OTel bridge (`examples/otel_bridge.py`) fed real spans; Hermes bridge exercised against a real install | **Not yet exercised** (`STATUS.md`) — do not claim |
| Trust event | A proof actually used for handover / release / diligence / incident review | **Zero observed** — this is the purchase trigger to hunt for |

**Rule:** report a funnel stage only when it has a dated, sourced count. Until then, write "unmeasured" / "zero observed".

## 4. Candidate models — ranked hypotheses, none adopted

These are **test designs, not a price list**. No model may be marketed until its experiment ( §6 ) produces evidence.

| Rank | Model | Why it might fit | Why it might fail |
|---|---|---|---|
| 1 | **Transactional trust-event packages** (D-013) — one verified handover / release / diligence evidence pack | Value concentrates at consequential moments; matches local-first (proof travels, no host needed) | Rare events → low volume; hard to discover buyers without a hosted surface |
| 2 | **Open core / support & hardening** — MIT core stays free; paid integration, audit-prep, or SLA help | Preserves dev-tool adoption; monetizes expertise, not access | No demand signal yet; risks looking like abandonware if support is thin |
| 3 | **Hosted verifier / anchoring service** (later) — optional tip anchoring + hosted proof archive | Natural paid layer once `habitat.anchor` has real users | Requires the production backend that does not exist today; build cost before revenue |
| 4 | **Seat-based SaaS** | Familiar to buyers | Explicitly deprioritized by D-013; contradicts local-first positioning; no hosted product to seat anyone on |

**Explicitly rejected for now:** usage/seat pricing on the demo dashboard, paywalled verification
(`tools/verify_proof.py` must stay free and stdlib-only — it is the trust anchor), and any "enterprise edition"
label without a deployed enterprise feature behind it.

## 5. Infrastructure cost honesty

Habitat is cheap *because* it is local-first. Say so precisely — and say what is not free.

| Layer | Cost today | Honest caveat |
|---|---|---|
| Local library/CLI | **$0 runtime** — stdlib + SQLite only; single-file proof verifier copies anywhere | Your laptop/disk; backups are your job (`habitat backup/restore` exists, untested at scale) |
| Optional signing | `cryptography` extra (MIT/BSD deps) | Key management is **your** responsibility — no runbook yet (see `RELEASE_ACCEPTANCE_REPORT.md` outstanding) |
| Persistent backend (if you self-host `habitat serve`) | A small VPS / persistent host — order of **single-digit USD/month** for a tiny SQLite service | **Not deployed today.** SQLite on ephemeral filesystems loses the ledger; TLS + network restriction are manual (see `VERCEL.md`). This is an owner infra decision, not a product feature. |
| Vercel web tier | Hobby/free tier covers a landing + demo inspector; production domain/analytics may require paid plan | Vercel is **presentation only** — it does not host the ledger. Do not budget Vercel as the backend. |
| OTel / observability you already pay for | Unchanged — Habitat absorbs spans, it does not replace your backend | No new observability bill, but also no observability value claimed |

**No margins, CAC, LTV, or "projected revenue" figures appear in this file — because there is no data to compute them from.**
Any cost number above is an order-of-magnitude operating cost, not a business forecast.

## 6. Experiments to run before charging anything

From `PROJECT_MAP.md` H1–H5 (all unvalidated; none executed as of 2026-11-08):

1. **Cold takeover** — give a stranger a repo + Habitat; can they verify a claim without help?
2. **Truth decay** — does evidence survive agent/handoff changes better than prose docs?
3. **Agent switching** — does the proof stay valid when the producer changes?
4. **Broken-project rescue** — can a proof pack speed up reconstructing what actually happened?
5. **Buyer test** — will anyone pay for a trust-event pack, and how much? (Interview-first; no landing-page pricing theatre.)

**Kill / pivot criteria:** if, after real attempts, no trust event is observed, the honest conclusion is that
Habitat is a well-built open-source tool with no business yet — publish that, don't dress it up.

## 7. What this project will never claim (until evidence exists)

- Users, revenue, conversion, growth, or market share of any kind.
- A hosted tier, SLA, or support commitment.
- That the demo dashboard is a product you can buy access to.
- Prices. There are none.
