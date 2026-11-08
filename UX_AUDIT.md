# Habitat — Phase 3 UX Audit

**Date:** 2026-11-08
**Repo:** `buttercode101/Habitat` @ `fb8aefe7` (local clone `~/habitat-audit`)
**Live:** https://habitat-za.vercel.app (re-checked 2026-11-08)
**Companions:** `PRODUCT_IDENTITY.md`, `COMPETITIVE_BENCHMARK.md`, `PRODUCTION_READINESS_AUDIT.md`
**Method:** Code + docs inspection and hands-on CLI runs in a scratch DB (`init → status → doctor → run → claim → verify → prove`), plus live-site fetches. Every defect below cites observed evidence. Anything not exercised is listed under *Not verified* — not asserted.

---

## 0. Headline verdict

Habitat's UX is **honest, small, and CLI-first — and its first-run path is broken in exactly the place the README advertises.** The single most important discovery of this audit:

> Following the README's headline command (`habitat prove --run-id run-42 …`) on a freshly initialized Habitat **fails** (`rejected / no_matching_trusted_action`, exit 1), because no action with `run-42` exists and nothing in the quickstart creates one. The command only works if you first run `examples/prove_run.py` (which seeds its own throwaway DB) or hand-record an action through internals the README never mentions.

The product's signature strengths are real and verified: the tamper-simulation proof inspector, the `UNVERIFIED` Rosendäl card, the six-level assurance copy, and the zero-install verifier (`tools/verify_proof.py` → `VALID` on the checked-in Greenlight proof). The weaknesses are almost all **first-run and error-path** issues, not concept issues — which makes them cheap to fix relative to their impact.

**UX score (this audit's judgement, not a measurement):** CLI happy path once seeded: strong. CLI first-run / error paths: weak. Web demo surface: strong. Web live surface: nonexistent (demo fallback, disclosed). Docs: thorough but undiscoverable and, in the README, incomplete at the install step.

---

## 1. Journey map

Stages per the brief: **install → configure → ingest → record → prove → export → verify**, plus the dashboard-vs-CLI comparison.

### 1.1 Install

| | Evidence |
|---|---|
| Package | `habitat 1.3.0`, zero runtime deps, optional `cryptography` for Ed25519 (`pyproject.toml`). Python ≥3.10. |
| README quickstart | Says *"Install the project according to the repository's packaging configuration, then run: `python -m pytest -q`"*. **There is no `pip install …` command anywhere in the README quickstart** (README.md:57–61). A first-time reader is not told the package name, the `habitat[signing]` extra, or that `habitat` is a console script. |
| Verified locally | `python3 -m habitat` works from the repo root (local package on `sys.path`). `python3 examples/prove_run.py` **fails with `ModuleNotFoundError: habitat`** unless the package is installed for that interpreter or `PYTHONPATH=.` is set — because running a script puts `examples/` (not the repo root, not cwd) at `sys.path[0]`. In this environment the editable install is bound to Python 3.13 while `python3` is 3.14, so the README's literal `python examples/prove_run.py` fails. This is partly an environment mismatch, but it exposes a real fragility: the examples have no path bootstrap and the README doesn't state the install prerequisite crisply. |
| Time to first proof | `PYTHONPATH=. python3 examples/prove_run.py` → `Standalone verification: VALID` (verified). That's the *actual* fastest path to a proof, but it is not the README's advertised path. |

**Friction:** The install step is the softest point in the whole journey. Everything downstream of it is better documented than this step.

### 1.2 Configure

| | Evidence |
|---|---|
| Entry | `habitat init --config examples/simple.yaml` (verified: `Initialized Habitat demo at …`). `examples/simple.yaml` is a good minimal example (3 jobs, one disabled). |
| Config format | Hand-rolled YAML subset parser (`habitat/config.py`, 51 lines): supports top-level scalars + a `jobs:` list with 2-space indent. Not full YAML — no nesting beyond jobs, no flow syntax, comments stripped naively. `validate_config` checks `id`/`name`/job shape, duplicate job IDs, `enabled` bool, `command` string. |
| Silent-misconfig risks | `schedule` values (`"every 30 sec"`, `"every 1 hour"`) are **never parsed or validated** — `runtime.py` runs enabled jobs on `run`/`--watch`, schedule strings are inert display text. A user who believes `schedule` drives the scheduler will be silently wrong. Unknown top-level keys are ignored silently. There is no `habitat config validate` / dry-run; the only feedback is an exception from `init` (format unclear — a raw `ValueError` traceback, uncaught in `cmd_init`). |
| Doctor | `habitat doctor` exists and is genuinely useful (DB, schema version, hash-chain integrity, jobs, agents, Python version). **But on a completely fresh, healthy local install it reports `NEEDS ATTENTION` (exit 1)** because `signing_secret` is unset (`doctor.py:23–24`). For the loopback-only local default, no secret is needed to use Habitat — the check presents a local-dev setup as unhealthy. Verified: fresh `init` → `doctor` → `✗ signing_secret … NEEDS ATTENTION`. Severity conflation: one check is about *signed remote ingestion*, the verdict is about *the installation*. |

### 1.3 Ingest (events)

| | Evidence |
|---|---|
| Paths | (a) `habitat serve` + `POST /v1/events` (HMAC-signed by default, 256 KiB cap, duplicate-ID rejection); (b) `habitat event --file/--json` CLI wrapper; (c) OTel bridge `events_from_spans()` (`examples/otel_bridge.py`, verified: emits a `job.completed` event with `run_id=trace-123`); (d) Hermes/AgentScope example scripts. |
| CLI ergonomics | `habitat event --help` gives no example payload. `--json` defaults to `""`, so a bare `habitat event` sends an empty body and fails with `{"accepted": false, "error": "invalid_json"}` — correct behaviour, poor guidance. Secret env vars default silently to `HABITAT_WEBHOOK_SECRET` / `HABITAT_AGENT_SECRET`; if unset, signing is skipped and (unless `--no-signature` semantics are understood) the event is rejected with `invalid_signature` — there is no hint that the secret is missing. |
| Server errors | HTTP layer is good: `401 authentication_required`, `429 authentication_rate_limited` with `Retry-After`, `413 event_too_large`, `400 invalid_json`-family codes (`server.py`). These are machine codes, not human explanations (see §4). |
| End-to-end proof | `examples/send_event.py` path is documented in `examples/README.md` §2 (two terminals, `habitat serve` + sender). Not exercised in this audit (would require a running server + matching secrets); the OTel path was exercised instead. |

### 1.4 Record (jobs / run)

| | Evidence |
|---|---|
| `habitat run` | Runs enabled jobs once (verified: 2 enabled jobs ran `ok`, 1 disabled job `skipped`). `--watch --interval` exists. |
| Signals | A fresh run of `examples/simple.yaml` immediately raises a `disabled_but_expected` warning ("Weekly audit is disabled but has a schedule") and flips habitat status to `degraded`. This is *correct* signal behaviour — and a questionable first-run impression: the shipped example config produces a warning on its first run with no explanation of what to do about it. |
| `status` / `inspect` | `status` prints clean JSON counts. `inspect` dumps `habitat.__dict__` + jobs + signals as raw JSON — including internal fields (`habitat_id`, `failure_streak`, timestamps) with no summary layer. For a supervision tool, the human-readable surface is thin: no "what needs my attention" summary outside the raw signal list. |
| The pre-init cliff | **Before `init`, `habitat status` and `habitat run` die with an uncaught `RuntimeError: No Habitat initialized` traceback** (verified, full stack trace, exit 1). `habitat prove` in the same state returns a clean `{"error": "No Habitat initialized"}` JSON. Error handling is inconsistent command-by-command (see UX-02). A new user who runs `habitat status` before `init` — the most natural first command — gets a Python traceback from a product whose entire brand is rigour. |

### 1.5 Prove (claim → verify)

| | Evidence |
|---|---|
| Two commands | `habitat claim` (create) + `habitat verify` (check) vs `habitat prove` (create + verify + export in one). The distinction is not explained in `--help` for either; `prove`'s help says one line, `claim`/`verify` have no `help=` at all. Users must read `__main__.py` to learn the difference. |
| The README fatal flaw | `habitat prove --run-id run-42 --claim "deployed v1.2.3 to production" -o proof.json --card` on a fresh DB → `{"status": "rejected", "evidence": {"reason": "no_matching_trusted_action"}, "error": "claim_not_verified"}`, exit 1, **no proof.json, no proof.md written**. The error tells the user *what*, not *what to do next* (record an action for that run first; here's how). Verified in scratch DB. |
| `verify` UX | `habitat verify` with no claims → `No claim found`, exit 1. No hint that `habitat claim` creates one. With a claim whose evidence doesn't match, the JSON evidence object (`reason`, `observed`) is actually informative — the best error content in the CLI — but it is raw JSON with no concluding sentence. |
| `--card` without `-o` | `cmd_prove` writes `proof.md` (card) even when no `-o proof.json` was given, and the card's embedded instruction is `python tools/verify_proof.py proof.json` — referencing a file that was never written (see UX-09). |

### 1.6 Export

| | Evidence |
|---|---|
| `habitat proof <id> -o proof.json` | Writes *only* the portable bundle (verified design intent in `ADOPTION.md`; code at `__main__.py:131–161`). Clean separation from the DB. |
| `habitat prove -o … --card` | Writes bundle + markdown proof card (verified output from `prove_run.py`: claim, status, run/job, evidence source, digest, assurance footer). The card is a genuinely good artifact for PRs/tickets. |
| Signing | `--signing-key-env/--key-id/--agent-id` flags exist; signing requires the optional `cryptography` extra. The key must be base64 Ed25519 in an env var — documented in `VERIFY_PROOF.md`, but there is no key-*generation* helper (`habitat keygen` or docs snippet), so the signing journey starts with "go figure out how to make an Ed25519 key". |
| Dashboard export | `habitat generate -o dashboard.html` produces a static snapshot. It carries **no generation timestamp**, so a user cannot tell how stale it is, and there is no regenerate affordance (see UX-19). |

### 1.7 Verify (consumer side)

| | Evidence |
|---|---|
| Zero-install verifier | `python tools/verify_proof.py proof.json` — single stdlib file. Verified `VALID` (exit 0) on `proofs/greenlight-9dc5a007.json` with the full six-level assurance object in the output. This is the product's best DX moment and it works. |
| Missing-file behaviour | `tools/verify_proof.py nonexistent.json` → **uncaught `FileNotFoundError` traceback** (verified). The consumer-facing tool — the one handed to auditors and CI — crashes ugly on the most basic error. Also no `--help`/usage; malformed JSON handling not exercised but the structure-check error list suggests it's handled for content errors, not file errors. |
| Verdict semantics | Output separates `valid`, `verdict`, `ledger_integrity`, `scope: "bundle-integrity-and-internal-consistency"`, `authenticity: "not-established"`, and the six assurance fields. Exemplary honesty. `VERIFY_PROOF.md` explains it well. The one gap: the output could state, in one line, "this does NOT prove the claim is true in the world" — the assurance object implies it, the card says it, but the terminal output doesn't (see §5). |

### 1.8 Dashboard vs CLI — two surfaces, two products?

| Dimension | CLI (`habitat`) | Native HTML (`habitat serve` / `generate`) | Web (Next.js, live) |
|---|---|---|---|
| What it shows | Everything, as JSON | Jobs, signals, claims, recent actions, KPIs (jobs enabled / ok / failed / needs attention) | Claims + proof inspector only |
| Signals | Raw list in `inspect` | "Needs attention" panel, severity badges, all-clear state | **Not surfaced at all** — no signals, jobs, or agents view |
| Empty states | `[]`, `No claim found` | `No jobs configured.` / `No recent actions.` / `No claims recorded yet.` / `All clear. Nothing needs attention.` — genuinely good | Live empty state exists (`No claims recorded yet…`) but is unreachable while the backend is down; demo mode masks it |
| Actions | Full command set | Links: Inspect claim, Verify now, Proof JSON | Claim cards, Inspect, "Verify now" (links to a **raw JSON API response**, not a verdict page — see UX-12) |
| Freshness | Always live (queries SQLite) | `serve` = live; `generate` = snapshot with no timestamp | Demo = checked-in artifact; explicitly disclosed |
| Trust signal | `doctor` (with the secret-severity flaw) | Ledger/status KPIs | `UNVERIFIED` card, tamper demo, assurance boundary section |

**The parity gap that matters:** the web dashboard — the surface a buyer actually sees — cannot show supervision signals, job health, or the action ledger. It is a *proof gallery*, not a supervision surface. The native dashboard does all of that but requires running `habitat serve` yourself, which the web marketing funnels away from ("Open dashboard" → Vercel demo). A user who wants the real product must discover the native surface from `examples/README.md` §1 (`habitat generate`) — it is not linked from the landing page.

---

## 2. Developer experience summary

**What's genuinely good (verified):**
- Zero runtime deps; `init → run → status → doctor` all work in seconds on a fresh DB.
- `examples/prove_run.py` is a real end-to-end proof in one script (`VALID` verified).
- OTel bridge is dependency-free and reuses `trace_id → run_id` (`otel_bridge.py` verified).
- Proof exchange is a single command each side (`habitat proof … -o`, `verify_proof.py`).
- `doctor` as a concept; hash-chain integrity as a check.
- Proof card output is copy-paste-ready for PRs.

**What's friction (verified above):**
- README install step has no `pip install` command; examples need an installed package or `PYTHONPATH`.
- The advertised `habitat prove` quickstart cannot succeed on a fresh DB (no seed path).
- Pre-init commands traceback instead of guiding.
- `doctor` fails a healthy local install over a remote-ingestion concern.
- No key-generation helper for the signing journey.
- `prove` vs `proof` vs `claim`+`verify`: three overlapping verbs, no in-CLI explanation.
- Config `schedule` is decorative; no config dry-run.
- 34 root-level `.md` files, no hosted docs, no index — discoverability is the DX tax (see §6).

---

## 3. Error & empty states — inventory

### 3.1 CLI (verified by running)

| Input | Output | Exit | Assessment |
|---|---|---|---|
| `status`/`run` before `init` | Python traceback (`RuntimeError: No Habitat initialized`) | 1 | ❌ Traceback; should be a one-line "No Habitat initialized — run `habitat init --config …`". |
| `prove` before `init` | `{"error": "No Habitat initialized"}` | 1 | ⚠️ Clean but unactionable. |
| `verify` with no claims | `No claim found` (plain text, not JSON) | 1 | ⚠️ Inconsistent format with other commands; no next-step hint. |
| `proof <nonexistent>` | `{"error": "claim_not_found"}` | 1 | ⚠️ Clean, unactionable. |
| `prove` with unmatched run | JSON `rejected / no_matching_trusted_action / claim_not_verified` | 1 | ⚠️ Best content in the CLI, still no "record an action first" guidance. |
| `verify_proof.py <missing file>` | `FileNotFoundError` traceback | 1 | ❌ Consumer-facing crash. |
| `doctor` fresh local install | `NEEDS ATTENTION` (secret unset) | 1 | ❌ False alarm for the default local setup. |
| `event` with bad/missing signature | `{"accepted": false, "error": "…"}` | 1 | ✅ Structured; could name the missing env var. |

Pattern: commands that go through `cmd_proof`/`cmd_prove` catch exceptions and emit JSON; `cmd_status`, `cmd_run`, `cmd_inspect`, `cmd_init` do not. The fix is a top-level handler that converts `RuntimeError("No Habitat initialized")` into the same JSON shape + a hint, everywhere.

### 3.2 HTTP API (`server.py`)

Machine codes: `authentication_required` (401), `authentication_rate_limited` (429 + `Retry-After: 60`), `event_too_large` (413), `invalid_json` / `unsupported_event_type` / `habitat_id_mismatch` / `unknown_job_id` (400), `claim_not_found` (404), `not_found` (404). Consistent, documented in `PROTOCOL.md`, but a client developer must map codes to meanings themselves — no `message` field, no docs link in the body.

### 3.3 Web

| State | Behaviour | Assessment |
|---|---|---|
| Backend down | Demo mode with explicit banner ("Live backend unavailable… Showing a checked-in Rosendaltown proof artifact"). Verified live. | ✅ Best-in-class honesty; the disclosure is prominent, specific, and repeated in the footer. |
| Backend up, no claims | `No claims recorded yet. Habitat will surface them here…` | ✅ Good empty state (code-read; not live-verifiable while backend is down). |
| Claim page, bad ID / backend error | `Habitat could not load this proof.` + the raw fetch error message (`Habitat API returned 404`) | ⚠️ Leaks an internal-ish message; contradicts the generic-error policy stated in `VERCEL.md`. Should say "claim not found or backend unreachable" + what to check. |
| 404 | Custom page ("This proof path does not exist."), verified live (404). | ✅ Good copy; inline styles diverge from the design system (cosmetic). Note `/proofs` (plural) 404s while proof files live under `/proofs/…` — a plausible user guess lands on the 404. |
| Proof inspector | `READY` → `INTEGRITY VERIFIED` / `DIGEST MISMATCH`, tamper simulation, reset, download. | ⚠️ See §5: the browser "verify" checks only the digest, but the label claims integrity verification. |
| `/evidence` | 2 reconciled artifacts + manifest + `verify-all.sh` download. Verified live. | ✅ Strong provenance copy ("Proofs we can actually stand behind"). |
| Landing hero | "UNVERIFIED — external commit not independently resolved" on the Rosendäl card. | ✅ The honesty *is* the UX. |

### 3.4 Native HTML dashboard (`generate.py`)

Empty states present for jobs/actions/claims/signals (quoted in §1.8). No "generated at" timestamp. Tables use `min-width: 650px` with horizontal scroll on small screens — acceptable, unverified on device.

---

## 4. Verification explanations — does the UI teach the boundary?

**Where it works well (verified):**
- `VERIFY_PROOF.md`: the six assurance levels are defined plainly; `valid: true` scope statement is exact.
- Landing page "Every proof has a boundary" section: structural/integrity/consistency ✓, publisher trust/external truth —.
- Proof card footer: "External truth and publisher trust are not established by this card alone."
- Claim page: "Interpretation boundary" notice.
- `/evidence`: "Not external truth" card.
- Verifier output: `scope`, `authenticity`, full assurance object.

**Where it breaks down:**

1. **ProofDemo overclaims (the one real honesty defect in the UI).** The browser demo computes *only* a SHA-256 digest comparison (`ProofDemo.tsx: digest()`), then displays **`INTEGRITY VERIFIED`**. Digest equality is not the six-level verification the product teaches everywhere else — it doesn't check structure, claim/ledger consistency, or even the verifier's canonicalization rules (the JS `canonical()` differs from the Python `_canonical()` in `ensure_ascii` handling and doesn't exclude `signature`). A user who "verifies" in the browser and then runs `tools/verify_proof.py` could get a different answer on edge-case input. For a product whose anti-drift rule is *"never make the project look more complete than it actually is"* (D-014), the demo's label should say `DIGEST MATCHES` — which, notably, is what the demo's own sub-copy already says ("Digest matches."). The big label contradicts the small print.
2. **Vocabulary drift across surfaces.** Verifier: `publisher_trust: not-assessed`, `external_truth: not-established`. Native proof inspector (`proof_ui.py:_assurance`): both `unknown`. Landing page: `—`. Proof card: prose. Same concepts, four vocabularies. A user comparing the CLI verifier output to the native inspector will see different words for the same state.
3. **`present-unverified` is well handled in docs, invisible in the demo.** The demo proof has no signature; the demo never shows what a signed-but-unverified proof looks like — the exact state a consumer will hit first in the wild.
4. **No "what would change this verdict" guidance.** Nowhere does any surface answer: *I got `inconclusive` — what evidence would make this `verified`?* The claim evidence JSON contains `reason` codes, but no surface translates them ("`run_id_required_for_ambiguous_trusted_verification` → supply `--run-id`"). This is the single most valuable explanation the product could add, because `inconclusive` is the honest-but-confusing verdict.

---

## 5. Integration docs gaps

| Integration | Docs state | Gap (evidence) |
|---|---|---|
| OTel | `OTEL.md` + `examples/otel_bridge.py` (verified runs). Boundary stated ("absorb spans, don't replace backend"). | Smallest gap. Missing: a *real collector/exporter* example (only hand-built span dicts); no note on GenAI semconv attribute churn (flagged in benchmark §7, not in `OTEL.md`). |
| Hermes | `examples/hermes_bridge.py`, `hermes_hmac_adapter.py`, `hermes_post_action.sh` — production-shaped. | **`STATUS.md` admits the bridge is "not claimed live until exercised against a real Hermes installation" — but nothing at the point of use says this.** A user reading the example files has no in-file caveat. Needs a header comment + README flag. |
| AgentScope | `examples/agentscope_source.md`, `examples/policy_wiring.md` (presets). | Same caveat problem; also the policy presets are only reachable via code (`verify_claim(..., policy=…)`), with no CLI flag — a CLI user cannot apply `no_drift_skip` at all. |
| LangChain / LangGraph | Named in `ADOPTION.md` as the audience ("complementary to LangSmith, Langfuse…"). | **No example, no adapter, no snippet.** The benchmark (§8) notes time-to-first-trace parity with LangSmith as a goal, but there is no LangChain-shaped walkthrough to judge by. |
| GitHub | `--github-issue` evidence adapter (`__main__.py`); `GitHubIssueEvidenceAdapter`. | No end-to-end example (no `.github` workflow sample, no walkthrough). The `verify-proof.yml` CI workflow exists in-repo but is not presented as a copy-me integration recipe. |
| Signing + trust | `SIGNING.md`, `VERIFY_PROOF.md`, `IDENTITY.md` — individually thorough. | No single runnable walkthrough: generate key → sign → verify with `TrustRegistry` → see `publisher_trust` flip. The journey is assembled from 3 files + code reading. |
| MCP / A2A | Aligned in prose (`ADOPTION.md`, benchmark §7). | No adapter, no example. Acceptable per D-002 (don't build), but the docs should say "not yet" explicitly rather than implying proximity. |
| Docs discoverability | 34 root `.md` files; `README.md` "Documentation" section lists 8. | No index, no hosted site, no "start here" reading order. `PROJECT_MAP.md`/`DECISIONS.md` etc. are project-internal but sit at the same level as user docs. A newcomer cannot tell which files are for them. |

---

## 6. UX defect register

Severity: **P0** = blocks or misleads first-time users. **P1** = significant friction / honesty risk. **P2** = polish / consistency.

| ID | Sev | Defect | Evidence | User impact |
|---|---|---|---|---|
| UX-01 | P0 | README headline `habitat prove --run-id run-42` fails on a fresh DB; no seed path documented. | Verified: `rejected / no_matching_trusted_action`, exit 1, no files written. README.md:63–72. | The documented first proof cannot be produced. Users will conclude the tool is broken. |
| UX-02 | P0 | README quickstart contains no install command. "Install the project according to the repository's packaging configuration" is not an instruction. | README.md:57–61. No `pip install habitat` / `pip install -e .` / `habitat[signing]` anywhere in quickstart. | Every new user stalls at step zero, or installs the wrong way (source checkout without install → `ModuleNotFoundError` in examples). |
| UX-03 | P1 | Pre-init `status`/`run`/`inspect` crash with Python tracebacks; error handling differs per command. | Verified tracebacks (`store.py:156`). `cmd_status`/`cmd_run`/`cmd_inspect` uncaught; `cmd_prove` catches. | First command most users try (`habitat status`) produces the worst output in the product. Brand damage. |
| UX-04 | P1 | ProofDemo labels a digest-only check "INTEGRITY VERIFIED". | `web/app/dashboard/ProofDemo.tsx`: `stateLabel = "INTEGRITY VERIFIED"`; `digest()` checks only `content_sha256`; JS canonicalization ≠ Python verifier. | Overclaims vs the product's own six-level model; browser and CLI verdicts can diverge on edge cases. Violates D-014 in spirit. |
| UX-05 | P1 | `habitat doctor` reports `NEEDS ATTENTION` on a healthy fresh local install (secret unset). | Verified. `doctor.py:23–24`. | Users learn to ignore `doctor` — the one diagnostic the product has. |
| UX-06 | P1 | `habitat prove --card` without `-o` writes a card that references a `proof.json` that was never written. | `__main__.py:219–223` (`card_path = … if a.output else Path("proof.md")`; card body hardcodes `verify_proof.py proof.json`). | Broken artifact; consumer runs a command that fails (`FileNotFoundError` traceback, UX-07). |
| UX-07 | P1 | `tools/verify_proof.py` crashes with traceback on missing/unreadable file; no usage message. | Verified `FileNotFoundError` traceback, exit 1. | The auditor-facing tool fails ugly on the most basic error. |
| UX-08 | P1 | Web "Verify now" links to a raw JSON API route, not a verdict page. | `web/app/dashboard/page.tsx` ClaimCard: `<a href={/api/claims/…/verify}>Verify now</a>` → returns JSON to the browser. Same pattern in native dashboard. | Users get a JSON blob instead of an explanation; the verification *experience* is a dead end. |
| UX-09 | P1 | Landing nav labels the demo "Live dashboard". | Live HTML: `<Link href="/dashboard">Live dashboard</Link>`; `/dashboard` renders `DEMO MODE`. Disclosure exists on the destination, not at the link. | Expectation mismatch at the exact moment of highest intent. (The demo disclosure itself is excellent once landed.) |
| UX-10 | P1 | No guidance for `inconclusive` / `rejected` verdicts: reason codes are never translated into "what to do". | `verify.py` reason codes; no UI/CLI translation layer. | The honest verdict becomes a dead end — precisely where a user needs teaching. |
| UX-11 | P1 | Hermes/AgentScope examples carry no in-file caveat that they're unexercised against a real install. | `STATUS.md:31` admits it; example files don't. | Users build on an unvalidated bridge believing it's proven. |
| UX-12 | P2 | `prove` vs `proof` vs `claim`+`verify`: three overlapping verbs, unexplained in help/README. | `__main__.py` help strings. | Users pick randomly; half the combinations don't do what they expect. |
| UX-13 | P2 | Config `schedule` is never validated or acted on by the scheduler; unknown keys silently ignored; hand-rolled YAML. | `config.py`; `runtime.py` runs enabled jobs regardless of schedule. | Silent misconfiguration; users believe jobs are scheduled when they're not. |
| UX-14 | P2 | Assurance vocabulary differs per surface (`not-assessed` / `not-established` / `unknown` / `—`). | `proof_verify.py` vs `proof_ui.py:_assurance` vs landing page. | Users can't build a stable mental model across CLI, inspector, and web. |
| UX-15 | P2 | `habitat generate` dashboard snapshot has no timestamp; no regenerate affordance. | `generate.py` — no generated-at output. | Stale snapshots are indistinguishable from live ones. |
| UX-16 | P2 | Claim page error state prints the raw backend fetch message. | `web/app/claims/[id]/page.tsx` catch block. Contradicts `VERCEL.md` generic-error policy. | Inconsistent trust posture; unhelpful to users. |
| UX-17 | P2 | `agent-add` prints the agent secret to stdout with no "store this securely, it won't be shown again" warning. | `__main__.py:264–272`. | Secret ends up in scrollback/logs; user doesn't know it's one-time. |
| UX-18 | P2 | `inspect` is a raw internal-state dump; no human summary. | `cmd_inspect` prints `__dict__`s. | Supervision product with no supervision summary in the CLI. |
| UX-19 | P2 | Example `simple.yaml` generates a `disabled_but_expected` warning + `degraded` status on first run, unexplained. | Verified run output. | First-run impression is "something is wrong" with no pointer to `signals` or how to resolve. |
| UX-20 | P2 | 34 root docs, no index/hosted docs; README lists only 8. | Repo listing; README.md:104–113. | Discoverability tax on every integration question (see §5). |

---

## 7. Prioritised improvements

Ordered by (user impact ÷ effort). Each item names the defect(s) it closes.

### P0 — before any launch push (the demo must survive first contact)

1. **Fix the first-run path (UX-01, UX-02).** Either (a) add `habitat demo` / `habitat seed` that records a sample action, or (b) rewrite the README quickstart as the *working* sequence: `pip install habitat` → `habitat init --config examples/simple.yaml` → `habitat run` → `habitat prove --run-id <the run id habitat run actually produced> …`. Option (b) is honest about the model; option (a) is better UX. Also state the `pip install` command and the `[signing]` extra explicitly. *Effort: small (docs) to medium (seed command).*
2. **Correct the ProofDemo label (UX-04).** `INTEGRITY VERIFIED` → `DIGEST MATCHES`; optionally add the structural/consistency checks the Python verifier does, or link out to `verify_proof.py` for the full check. One-line change that removes the only honesty defect in the UI. *Effort: trivial.*
3. **Add a docs index (UX-20).** A `docs/README.md` (or README section) with a reading order: Quickstart → Protocol → Verify → Signing → OTel → Hermes/AgentScope → Reference. Mark internal docs (PROJECT_MAP, DECISIONS, HANDOFF) as "project-internal" or move them. *Effort: small.*

### P1 — next iteration

4. **Uniform CLI error handling (UX-03, UX-07).** Top-level handler: `No Habitat initialized` → `{"error": "not_initialized", "hint": "habitat init --config <file>"}` on every command. `verify_proof.py`: catch file/JSON errors, print usage + clean error, exit 2. *Effort: small.*
5. **Actionable verdicts (UX-10).** A reason-code → explanation map (`no_matching_trusted_action`, `run_id_required_…`, `action_ledger_integrity_check_failed`, …) rendered in `verify`/`prove` output and on the claim page: what it means, what to do next. This single feature converts the product's most confusing moment into its best teaching moment. *Effort: medium.*
6. **Fix `doctor` severity (UX-05).** `signing_secret` → warning-level ("not required for local loopback use"), or split verdicts: "Local: HEALTHY / Ingestion: not configured". *Effort: trivial.*
7. **Fix `--card` without `-o` (UX-06).** Either require `-o` with `--card`, or embed the actual proof path the card references. *Effort: trivial.*
8. **A real "Verify now" verdict page (UX-08), and relabel the nav (UX-09).** A human-readable verdict view (the native `proof_ui.py` inspector already does this — surface it in the web tier instead of raw JSON). Nav: "Dashboard (demo)" until a backend exists. *Effort: medium.*
9. **Integration caveats + one LangChain-shaped example (UX-11, §5).** Header comments in Hermes/AgentScope examples ("not yet exercised against a real <X> install — see STATUS.md"); one `examples/langchain_bridge.py` mirroring `otel_bridge.py`'s shape. *Effort: small–medium.*

### P2 — polish backlog

10. **Unify assurance vocabulary (UX-14)** — pick the verifier's terms everywhere; map `unknown` → `not-assessed`/`not-established` in `proof_ui.py`.
11. **Explain `prove` vs `proof` (UX-12)** — one help line each; a "Commands" table in README. Consider `habitat prove` absorbing `proof`'s export-only mode explicitly (`--existing`).
12. **Config honesty (UX-13)** — warn on unknown keys; either validate `schedule` syntax or rename the field to `note` until a scheduler exists.
13. **Native dashboard timestamp + `generate` freshness (UX-15); claim-page error copy (UX-16); `agent-add` one-time-secret warning (UX-17); `inspect --summary` (UX-18); explain the example warning (UX-19)** — each small; batch as a "CLI/web copy pass".

---

## 8. Strengths to protect (do not regress)

- The tamper-simulation inspector — the most convincing 30 seconds in the product. Keep the mechanism; fix only its label (UX-04).
- The `UNVERIFIED` Rosendäl card and the demo-mode disclosure. This is the brand; every "improvement" above preserves it.
- The zero-install verifier and its six-level output. Verified working.
- The proof card. Verified good output.
- The `/evidence` provenance discipline ("Proofs we can actually stand behind") and `verify-all.sh`.
- Native dashboard empty states and the "Needs attention" panel. The web tier should *borrow* these, not the reverse.

---

## 9. Not verified (explicit unknowns)

- **Responsive / device behaviour**: per `RESPONSIVE_COMPATIBILITY_REPORT.md`, no Playwright matrix or physical-device pass exists. This audit did static source review only (skip links, aria labels, responsive breakpoints present in CSS; tables scroll on small screens). No claim is made about how it renders at 360px.
- **Accessibility beyond static review**: skip links, `aria-label`, `aria-current`, semantic landmarks observed in source/HTML. No screen-reader or keyboard-only run was performed.
- **Live claim page / live dashboard**: unreachable while the backend is down; reviewed by code only. The live `/dashboard` demo and `/evidence` were fetched and verified by content.
- **Hermes/AgentScope/LangChain integrations**: not exercised (no such installs available). OTel bridge and local CLI paths were exercised.
- **User testing**: none exists. Every severity above is expert judgement from evidence, not observed user behaviour. The Truth Layer experiments in `PROJECT_MAP.md` remain unexecuted, so H-U1–H-U3 (PRODUCT_IDENTITY §2) are still hypotheses.
- **Stale cache**: live homepage `age` header was `253480s` (~2.9 days) at check time — H-005 from the readiness audit is worsening, not fixed. A user may see older landing copy than the repo contains.

---

## 10. Sources

Repo: `README.md`, `habitat/__main__.py` (428 LOC), `habitat/config.py`, `habitat/doctor.py`, `habitat/server.py`, `habitat/generate.py`, `habitat/proof_ui.py`, `habitat/proof_card.py`, `habitat/verify.py`, `habitat/proof_verify.py` + `tools/verify_proof.py`, `habitat/events.py`, `examples/{README,simple.yaml,prove_run,otel_bridge,hermes_bridge,proof_exchange.md,policy_wiring}.md/py`, `ADOPTION.md`, `VERIFY_PROOF.md`, `STATUS.md`, `VERCEL.md`, `web/app/**` (`page.tsx`, `dashboard/page.tsx`, `dashboard/ProofDemo.tsx`, `evidence/page.tsx`, `claims/[id]/page.tsx`, `not-found.tsx`, `web/lib/habitat.ts`). Live site: `/`, `/dashboard`, `/evidence`, unknown route (2026-11-08). Hands-on: scratch-DB CLI runs (`init/status/doctor/run/claim/verify/prove`), `verify_proof.py` on checked-in proofs, `prove_run.py` and `otel_bridge.py` with `PYTHONPATH=.`.
