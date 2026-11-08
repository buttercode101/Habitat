# Habitat — Phase 4 Design System

**Date:** 2026-11-08
**Repo:** `buttercode101/Habitat` @ `fb8aefe7` (local clone `~/habitat-audit`)
**Companions:** `PRODUCT_IDENTITY.md` (Phase 1), `COMPETITIVE_BENCHMARK.md` (Phase 2), `UX_AUDIT.md` (Phase 3 — defect IDs UX-01…UX-20 cited throughout)
**Status:** Proposal — tokens/spec only, no code changed. Where this spec conflicts with shipped CSS/Python, the shipped value is noted as *current* and the spec value as *proposed*.

> **Anti-drift rule (D-014, Permanent):** *Never make the project look more complete than it actually is.* Every rule below serves it: verdicts never read stronger than the check that produced them, demo surfaces are labelled demo at the point of intent, and `inconclusive` is always paired with what would change it.

---

## 0. Design principles (inherited, not invented)

1. **Evidence before decoration.** The product answers one question — *what evidence does the system actually have for that claim?* (`PRODUCT_IDENTITY.md` §1.2). UI that cannot cite its evidence layer (ledger, digest, signature, TrustRegistry) does not ship.
2. **Boundary honesty is the brand.** `UNVERIFIED` on the Rosendäl card, the demo-mode disclosure, and `present-unverified` are features to protect (`UX_AUDIT.md` §8), not embarrassments to soften.
3. **CLI first, dashboard second, marketing third** — in that order of authority. A claim that renders differently in terminal, native HTML, and web is a defect (UX-14), not a theme choice.
4. **No hosted control plane, no framework lock-in.** The design system is plain CSS custom properties + system fonts, mirroring the zero-runtime-dep Python ethos (`PRODUCT_IDENTITY.md` §1.6). No component library, no webfont dependency for the CLI/native surfaces.

---

## 1. Tokens (single source of truth — proposed)

Current state has **three near-identical token sets** that must converge: web (`globals.css`: bg `#090909`, accent `#b8f36b`), native dashboard + inspector (`generate.py` / `proof_ui.py`: bg `#090a0c`, accent `#d8ff63`, `--ok:#67e8a5`, `--warn:#f5c451`, `--bad:#ff6b6b`). The web tier has **no semantic ok/warn/bad tokens at all** — verdict colour is improvised per component (`status.ok` reuses accent; `status.attention` reuses `#f0c36a`). That is the root of UX-04 and UX-14.

### 1.1 Colour

| Token | Value | Role | Current |
|---|---|---|---|
| `--hb-bg` | `#090909` | Page/terminal background | web `#090909` ✅ / native `#090a0c` ⚠️ → unify to `#090909` |
| `--hb-surface` | `#101012` | Cards, panels | web `#10100f` / native `#101216` → unify |
| `--hb-surface-2` | `#151513` | Raised / hover | web ✅ |
| `--hb-line` | `#292925` | Borders, dividers | web ✅ / native `#272b33` (bluish) → unify to warm neutral |
| `--hb-text` | `#f4f4f1` | Primary text | ✅ both |
| `--hb-muted` | `#9b9c95` | Secondary text (≥ 4.5:1 on bg) | web `#a8a9a2` body / `#77786f` meta ⚠️ (see §7) |
| `--hb-faint` | `#6d6e68` | Captions, mono metadata — **never sole carrier of a verdict** | web ✅ |
| `--hb-accent` | `#b8f36b` | Brand accent, primary action, focus ring, "established" check marks | web ✅ / native `#d8ff63` ⚠️ → unify to `#b8f36b` |
| `--hb-accent-ink` | `#0a0a09` | Text on accent | ✅ |
| `--hb-verified` | `#67e8a5` | **Verdict: verified** (see §5) | native only — **adopt everywhere** |
| `--hb-inconclusive` | `#f5c451` | **Verdict: inconclusive / attention** | native `--warn` / web `#f0c36a` → unify to `#f5c451` |
| `--hb-rejected` | `#ff6b6b` | **Verdict: rejected / invalid / digest mismatch** | native `--bad` only — **adopt everywhere** |
| `--hb-not-established` | `#8d8e87` | **Assurance state: not established / not assessed** — neutral grey, deliberately *not* green | new; replaces `—` and `unknown` (UX-14) |

Rules:
- **Green means a check passed, nothing more.** `--hb-verified` is reserved for verdicts/checks that actually ran. It is never used for brand decoration on a claim card (today's hero proof window paints the whole status line accent-green — that must stop; see §6.3).
- **Grey is a first-class verdict colour.** "Not established" must be visible, not a dash. The Rosendäl `UNVERIFIED` treatment is the reference.
- Verdict colour is always paired with a text label + icon shape (not colour alone — §7). Colour is redundant encoding, never the only encoding.

### 1.2 Typography

| Token | Value | Use |
|---|---|---|
| `--hb-font-ui` | `Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif` | All UI text (already uniform across web + native ✅ — keep) |
| `--hb-font-mono` | `ui-monospace, "SF Mono", "Cascadia Code", Menlo, Consolas, monospace` | Digests, IDs, commands, JSON, file paths — anywhere a user copies or compares |
| Display | `clamp(42px, 7vw, 78px)`, `line-height .96`, `letter-spacing -.065em`, weight 800 | Hero / inspector H1 only |
| H2 | `clamp(30px, 4vw, 48px)`, `-.045em` | Section heads |
| Body | 14–15px native dashboard / 16–18px marketing, `line-height 1.55–1.7` | — |
| Eyebrow/label | 11px, weight 800, `letter-spacing .12–.16em`, uppercase, `--hb-accent` or `--hb-faint` | Section kickers, panel heads, verdict labels |
| Mono metadata | 11px mono, `--hb-faint`, `overflow-wrap:anywhere` | Claim IDs, digests, run IDs (already the pattern ✅) |

Type rules:
- **Never set a verdict, digest, or command in the UI font.** Mono is the "this is evidence, copy it exactly" signal. (Today's `.mono` class does this in web; extend to native + CLI.)
- Display sizes are marketing-only. Dashboard/CLI never exceed 30px H1 (native `dashhead h1` is already 30px ✅).
- No webfont is loaded for native/CLI surfaces; Inter is a progressive enhancement over system-ui, never a requirement.

### 1.3 Spacing & radii

Adopt the web scale as canonical (native is close but ad hoc):

| Token | Value |
|---|---|
| `--hb-space-1…6` | 4, 8, 12, 16, 24, 32 (section rhythm 80–128px marketing / 36px dashboard) |
| Container | `width: min(1180px, calc(100% - 40px))` web; native `min(1120px, …)` → **unify to 1180px** |
| Radius | 8px controls, 10–12px cards/panels, 14–17px hero windows, 999px pills/status |
| Touch targets | Min 40px height (buttons already 40–42px ✅); 44px on ≤480px (already done in demo banner ✅ — extend to all buttons) |

### 1.4 Breakpoints (proposed, from current CSS)

| Token | Width | Behaviour |
|---|---|---|
| `--hb-bp-lg` | 900px | Marketing hero stacks; steps 4→2 cols; split sections stack |
| `--hb-bp-md` | 800px | Claims/proof grids 2→1 col; metrics 4→2; nav collapses to mobile menu |
| `--hb-bp-sm` | 480px | Single column everywhere; buttons full-width; rows stack (label above value) |

Native currently breaks at 760/460px — **align to 800/480** so web and native behave identically. Every table gets `min-width` + horizontal scroll container (native pattern, ✅ exists) rather than crushing columns.

---

## 2. CLI design language

The CLI is the primary surface (`PRODUCT_IDENTITY.md` §1.6). Its visual language must be teachable in one screen and consistent across all 15 commands (today it is not — UX-03, UX-10, UX-18).

### 2.1 Output contract (proposed)

Every command emits **one** of three shapes — never a fourth:

1. **Machine JSON** (default for `status`, `inspect`, `verify`, `prove`, `proof`, `event`): `{"ok": bool, "status": …, "error": null | "code", "hint": "…" | null, "data": {…}}`. The existing error codes (`claim_not_found`, `no_matching_trusted_action`, …) stay; a `hint` field is added (UX-03/UX-10).
2. **Human summary** (`--summary` / default for `doctor`, `run`, `init`): 3–6 plain lines, `✓`/`!`/`✗` glyphs (not colour — terminals vary), each line ending in the *next action* where one exists.
3. **Artifact paths** (`prove`, `proof`): `Wrote proof.json (digest sha256:…)` + `Wrote proof.md — verify: python tools/verify_proof.py proof.json`. The card always names the file that actually exists (closes UX-06).

**Hard rules:**
- **No traceback is ever user-facing.** A top-level handler converts known `RuntimeError`s (`No Habitat initialized`) into shape 1 with `error: "not_initialized"` and `hint: "run: habitat init --config <file>"` (closes UX-03). Unknown exceptions print `error: "internal"` + a one-line *"report with `habitat doctor` output"* — never a stack.
- **Exit codes:** `0` success/verdict reached, `1` verdict negative or user error, `2` usage error (bad flags, missing file — `verify_proof.py` on a missing path exits 2 with usage, not a traceback; closes UX-07).
- **Verdict line is always last and always plain words:** `Verdict: verified (evidence supports the claim in the local ledger) — not external truth.` (see §5.2). Machine consumers parse JSON; humans never have to decode `rejected/no_matching_trusted_action` alone.

### 2.2 Command taxonomy (closes UX-12)

| Verb | One-line contract (to appear verbatim in `--help`) |
|---|---|
| `habitat claim` | Create a claim against recorded evidence. Does not verify it. |
| `habitat verify` | Check an existing claim. Prints verdict + what would change it. |
| `habitat prove` | Claim + verify + export in one step. The first-run command. |
| `habitat proof` | Export an *existing* claim as a portable bundle. No verification. |

### 2.3 Reason-code → explanation map (closes UX-10 — the highest-value CLI change)

Every `verify`/`prove` failure renders `reason → meaning → next action`. Minimum map:

| Reason code | Meaning | Next action (printed) |
|---|---|---|
| `no_matching_trusted_action` | No recorded action matches this claim (wrong/missing `run_id`). | `Record the action first (habitat run / POST /v1/events), or pass the correct --run-id.` |
| `run_id_required_for_ambiguous_trusted_verification` | Multiple actions match; the run is ambiguous. | `Pass --run-id <id> to pin the claim to one run.` |
| `action_ledger_integrity_check_failed` | The local hash chain does not verify. | `Run habitat doctor. Do not export proofs from this ledger.` |
| `claim_not_verified` | The evidence does not satisfy the policy. | `See observed vs expected above; adjust the claim or the policy preset.` |
| `not_initialized` | No Habitat DB found. | `habitat init --config examples/simple.yaml` |

This table is data, not copy scattered through `verify.py` — one dict, used by CLI, native inspector, and web claim page alike.

---

## 3. Dashboard components (web + native share one spec)

Both surfaces render the same components from the same tokens; the web tier may add marketing chrome, never different verdict semantics.

### 3.1 Component inventory

| Component | Spec | Notes |
|---|---|---|
| **Verdict badge** | Pill, 10px/800 uppercase, token colour per §5, **always with text label** (`VERIFIED` / `INCONCLUSIVE` / `REJECTED`) | Never colour-only. Disposition: replaces `status.ok/attention` improvisation. |
| **Assurance row** | Label + state word from the closed vocabulary (§5.1) + token colour; six rows, fixed order | Replaces `—`, `unknown`, and prose-only states (UX-14). |
| **Claim card** | Verdict badge top-right; claim text 19–20px; mono meta (run/job/digest); actions: *Inspect*, *Verify now* (→ verdict page, §6.2), *Proof JSON* | Current claim card is close; add badge, remove raw-JSON "Verify now" (UX-08). |
| **Needs-attention panel** | Signal list with severity badge (`critical`/`warning` — native pattern ✅); empty state: *All clear. Nothing needs attention.* | Web tier must adopt this panel — today signals are invisible on web (`UX_AUDIT.md` §1.8 parity gap). |
| **KPI strip** | 4 tiles: jobs enabled / ok / failed / needs attention | Native ✅; web "metrics" show proof counts instead — align to supervision KPIs, proofs live in `/evidence`. |
| **Proof inspector** | Claim → evidence → integrity → assurance → boundary notice, in that order | The tamper-simulation interaction is protected (§8); only its labels change (§6.1). |
| **Boundary notice** | `border-left: 2px solid accent` + *"External truth and publisher trust are not established by this card alone."* | Already the proof-card footer ✅ — promote to a shared component used by claim page, inspector, and card. |
| **Empty states** | Card + one sentence + one next action. Reference copy: `No claims recorded yet. Habitat will surface them here once a claim is verified.` (web ✅) / `No jobs configured.` (native ✅) | Every list gets one before it gets data. |
| **Demo banner** | Persistent, above the fold, *"Demo data — checked-in proof artifact. Live backend unavailable."* + link to run locally | Exists ✅ on `/dashboard`; must also appear **at the nav link** (§6.3). |

### 3.2 Component rules

- **One card style.** `surface` bg, `line` border, 12px radius, 20–24px padding. No card invents its own border colour.
- **Hover is decoration, never information.** `translateY(-1px/-3px)` lifts (current) are fine; nothing may be *revealed* or *hidden* by hover.
- **Freshness or it didn't happen.** Every rendered surface states its data source and age: live (`habitat serve`, queried now), snapshot (`generated <timestamp>` — closes UX-15), or demo (`checked-in artifact, <date>`). No silent staleness.

---

## 4. Verdict colour language (the heart of the system)

### 4.1 The six assurance levels — closed vocabulary

One vocabulary, everywhere (closes UX-14). These words are the verifier's, extended to UI:

| # | Level | Established | Not established | Colour |
|---|---|---|---|---|
| 1 | `structural_validity` | `valid` | `invalid` | verified / rejected |
| 2 | `content_integrity` | `valid` (digest matches) | `invalid` | verified / rejected |
| 3 | `internal_consistency` | `valid` | `invalid` | verified / rejected |
| 4 | `signature` | `verified` | `absent` / `present-unverified` | grey / inconclusive |
| 5 | `publisher_trust` | `trusted` | `not-assessed` | grey (never green unless a `TrustRegistry` actually ran) |
| 6 | `external_truth` | — (verifier can never establish it) | `not-established` | grey, always |

Forbidden: `unknown`, `—`, `true` for publisher/external levels, and any boolean for levels 5–6. `present-unverified` must be *shown* in the demo (§6.1) — it is the state consumers hit first in the wild and today no surface renders it (UX_AUDIT §4.3).

### 4.2 Verdict colours (claim level)

| Verdict | Colour | Icon | Sentences that may accompany it |
|---|---|---|---|
| `verified` | `--hb-verified` `#67e8a5` | ✓ | "Evidence supports the claim **in the local ledger**." |
| `inconclusive` | `--hb-inconclusive` `#f5c451` | ! | "Evidence is insufficient. <What would change this verdict>." |
| `rejected` | `--hb-rejected` `#ff6b6b` | ✗ | "Evidence contradicts the claim, or the ledger does not verify." |
| Demo / not yet checked | `--hb-not-established` `#8d8e87` | ○ | "Demo data. Not a live verification." |

**The one-line boundary (closes UX_AUDIT §1.7):** every verdict, in every surface, is followed by exactly one of:

- Verified: *"This shows the claim matches evidence in the local ledger. It does not prove the claim is true in the world."*
- Inconclusive: *"This shows the evidence is insufficient — here is what would change the verdict: …"*
- Rejected: *"This shows the evidence does not support the claim. The claim and the evidence are both shown above."*
- Demo: *"This is a checked-in demo artifact, not a live check. Run `tools/verify_proof.py` for the real verdict."*

### 4.3 What colour must never do

- **Never** paint an unverified claim green (today's hero proof window — §6.3).
- **Never** use accent `#b8f36b` as a verdict colour where `--hb-verified` exists. They are different greens with different meanings; conflating them is how a digest-only check got labelled "INTEGRITY VERIFIED" (UX-04).
- **Never** let `inconclusive` wear red. `inconclusive` is honest, not broken — it is the product working as designed (`PRODUCT_IDENTITY.md` §1.4). Red is reserved for *contradicted* and *tampered*.

---

## 5. Motion

Keep exactly what the current CSS does — it is already restrained — and write it down so it doesn't grow:

| Element | Motion | Duration |
|---|---|---|
| Buttons | `background/border-color .18–.2s ease`, `translateY(-1px)` on hover, `box-shadow` lift on primary | 180–200ms |
| Cards / proof window | `translateY(-3px)` / settle-to-flat, shadow deepen | 250–350ms |
| Focus ring | Instant (no transition) — keyboard users must not wait for it | 0ms |
| Tamper simulation result | State text swaps; **no colour-flash animation** — a verdict changing is a reading event, not a celebration | 0ms |
| Page scroll | `smooth`, disabled under `prefers-reduced-motion` | — |

**Global rule:** `prefers-reduced-motion: reduce` disables all transform/shadow transitions and smooth scroll (already partially present in web CSS ✅ — extend to native `generate.py`/`proof_ui.py`, which have no such block today). Nothing animates the *meaning* of a verdict; motion is limited to affordance and depth.

---

## 6. Motion / accessibility (a11y)

### 6.1 Contrast

| Pair | Ratio (approx.) | Verdict |
|---|---|---|
| `#f4f4f1` on `#090909` | ~15:1 | ✅ |
| `#b8f36b` on `#090909` | ~11:1 | ✅ accent/focus safe |
| `#090909` on `#b8f36b` | ~11:1 | ✅ primary button |
| `#9b9c95` muted on `#090909` | ~7:1 | ✅ body secondary |
| `#77786f` meta on `#090909` | ~4.6:1 | ⚠️ **only for ≥12px non-essential text**; verdict-adjacent text must use `--hb-muted` or brighter |
| `#6d6e68` faint on `#090909` | ~3.9:1 | ❌ for text — captions/eyebrows only, always duplicated in plain words nearby |

### 6.2 Keyboard & structure

- Every interactive element reachable by Tab, visible focus ring: `2px solid --hb-accent, offset 3–4px` (web ✅ — port to native). No `outline: none` anywhere without a replacement.
- Skip link to main content (web ✅ `.skip-link` — port exact pattern to native pages, which lack it).
- Landmarks: `header`/`nav`/`main`/`footer`; one `h1` per page; panel heads as `h2` (native ✅).
- `aria-current="page"` on active nav (web ✅ observed), `aria-label` on icon-only controls.
- Verdict badges are text, not images — screen readers announce "Verdict: inconclusive", never a colour name.

### 6.3 What is **not** verified (do not claim)

Per `UX_AUDIT.md` §9: no screen-reader run, no keyboard-only pass, no 360px device test exists. This spec's a11y rules are static-review-derived. **Before any launch claim about accessibility:** run one keyboard-only pass (Tab through claim → inspect → verify → download), one screen-reader pass over the inspector, and one 360px render check. Record results in `RESPONSIVE_COMPATIBILITY_REPORT.md`.

---

## 7. Proposals for the P0s

### 7.1 P0-1 — First-run path: make the advertised command work (UX-01, UX-02)

**Problem (verified):** README's `habitat prove --run-id run-42 …` fails on a fresh DB (`no_matching_trusted_action`, no files written), and the quickstart contains no install command at all.

**Proposal (both, in this order):**

1. **Docs-only, immediate:** rewrite the quickstart as the *working* sequence and state install explicitly:
   ```
   pip install habitat            # add: pip install 'habitat[signing]' for Ed25519
   habitat init --config examples/simple.yaml
   habitat run                    # note the run_id it prints — that is your --run-id
   habitat prove --run-id <run_id from habitat run> --claim "…" -o proof.json --card
   python tools/verify_proof.py proof.json   # → VALID, exit 0
   ```
   The critical fix is `--run-id <the one habitat run produced>` — the README currently invents `run-42`, which no fresh ledger contains.
2. **Better UX, small build:** `habitat demo` (or `habitat seed`) that records one sample action through the real `store`/`events` path (not a fixture file), prints the exact next `prove` command with that run's real ID, and is clearly labelled as sample data in every artifact it creates. When it exists, the quickstart's step 3 becomes `habitat demo` and the invented `run-42` disappears.
3. **Guardrail:** `habitat prove` on an unmatched run must, instead of a bare `rejected`, print the §2.3 next action (`Record the action first…`) and exit 1 — so even an outdated README cannot produce a dead end.

**Design-system implication:** this is a *copy + CLI contract* fix, not a visual one. The design system's contribution is the §2.1 output contract (hint field, artifact-path lines) and the §2.3 explanation map — the first-run failure must be explainable in the system's own vocabulary.

### 7.2 P0-2 — Honest demo labelling vs the 6-level assurance model (UX-04, UX-09, UX-14)

**Problem:** ProofDemo computes only a SHA-256 digest comparison, then displays **`INTEGRITY VERIFIED`** — a label that claims the six-level verification the product teaches everywhere else, while its own sub-copy correctly says "Digest matches." It is the only honesty defect in the UI (UX-04). Separately, the landing nav calls the demo "Live dashboard" (UX-09), and four surfaces use four vocabularies for the same assurance states (UX-14).

**Proposal:**

1. **Relabel, don't rebuild.** `INTEGRITY VERIFIED` → **`DIGEST MATCHES`** (the sub-copy's own words — the demo already knows the truth). State line becomes: `Digest matches — this checks content integrity only. Full verification (structure, consistency, signature, trust): python tools/verify_proof.py proof.json`. The tamper interaction, reset, and download all stay — §8 protects them.
2. **Show the missing level.** Add a second demo state: a **signed-but-unverified** proof (`present-unverified`, level 4) rendered in `--hb-inconclusive` with the sentence *"A signature is present but has not been checked. Run the verifier with your TrustRegistry to assess publisher trust."* This is the state a real consumer hits first; the demo currently cannot produce it (UX_AUDIT §4.3).
3. **Fix the label at the point of intent.** Nav: `Live dashboard` → **`Dashboard (demo)`** until a backend exists; the destination banner stays. A user must not learn the truth only after clicking.
4. **One vocabulary.** Replace `unknown` (native inspector), `—` (landing), and prose-only states with the §4.1 closed vocabulary everywhere: `not-assessed` (publisher), `not-established` (external), `absent` (no signature). Mapping is mechanical; `proof_ui.py:_assurance` is the single edit point on the native side.
5. **Hero card discipline.** The marketing hero proof window currently paints its status line in brand green. Restyle it to the §5 palette: green *only* if the artifact it depicts is verified; the Rosendäl card keeps its grey `UNVERIFIED` treatment — it is the brand (§8), not a bug.

**Design-system implication:** §4.1 + §4.2 exist precisely so this class of defect becomes impossible to write: a component that only checks a digest can only emit `DIGEST MATCHES`, because `INTEGRITY VERIFIED` is not in the vocabulary.

### 7.3 P0-3 — Verification explanations: make `inconclusive` teach (UX-08, UX-10, UX-16)

**Problem:** The honest verdict is a dead end. Reason codes exist in JSON but no surface translates them; "Verify now" lands on raw JSON; the claim page prints a raw backend error.

**Proposal:**

1. **The verdict page.** "Verify now" (web + native) links to a human verdict view — reuse the native `proof_ui.py` inspector in the web tier — rendering: verdict badge → the §4.2 boundary sentence → per-reason explanation from the §2.3 map → the evidence (observed vs expected) → next action. Raw JSON becomes a *secondary* "View raw" toggle, never the destination.
2. **"What would change this verdict" is a required block** for every `inconclusive`/`rejected` render, fed by the reason map. Example for `run_id_required_…`: *"This claim matches 3 actions. Pin it to one run: `habitat verify --run-id <id>`."*
3. **Error copy rule.** Claim page errors: *"Claim not found, or the backend is unreachable. Check the claim ID, or run `habitat serve` locally."* Never the raw fetch message (UX-16). Same rule in CLI: no raw exception text, ever (§2.1).
4. **Terminal boundary line.** `verify_proof.py` output ends with the §4.2 sentence for its verdict — today the assurance object *implies* "not external truth" but the terminal never *says* it (UX_AUDIT §1.7).

**Design-system implication:** §2.3 (reason map as data) + §4.2 (boundary sentences) + §3.1 (verdict page component) are specified once and consumed by CLI, native, and web — one maintenance point, three surfaces.

---

## 8. Strengths to protect (do not regress while implementing)

- The tamper-simulation inspector — mechanism stays, only its label changes (§7.2).
- The `UNVERIFIED` Rosendäl card + demo-mode disclosure — the brand.
- The zero-install verifier and its six-level output — add the boundary line, change nothing else.
- The proof card — copy-paste-ready; fix only the `--card`-without-`-o` reference (UX-06).
- `/evidence` provenance discipline ("Proofs we can actually stand behind") + manifest + `verify-all.sh`.
- Native empty states and the "Needs attention" panel — the web tier borrows these, not vice versa.

## 9. Implementation order (design-system view)

1. Tokens: unify accent/bg/line across web + native; add `--hb-verified/inconclusive/rejected/not-established` to web (closes UX-04, UX-14 mechanically).
2. §2.3 reason map as data + §2.1 output contract (closes UX-03, UX-07, UX-10).
3. ProofDemo relabel + `present-unverified` state + nav label (closes UX-04, UX-09).
4. Verdict page + freshness stamps (closes UX-08, UX-15).
5. First-run rewrite, then `habitat demo`/`seed` (closes UX-01, UX-02).

## 10. Sources

Repo: `web/app/globals.css`, `habitat/generate.py`, `habitat/proof_ui.py`, `habitat/proof_card.py`, `habitat/__main__.py`, `habitat/verify.py`, `habitat/proof_verify.py`, `tools/verify_proof.py`, `web/app/dashboard/ProofDemo.tsx`, `web/app/claims/[id]/page.tsx`, `RESPONSIVE_COMPATIBILITY_REPORT.md`. Prior phases: `PRODUCT_IDENTITY.md`, `COMPETITIVE_BENCHMARK.md`, `UX_AUDIT.md` (§§1.7–1.8, 3–8).
