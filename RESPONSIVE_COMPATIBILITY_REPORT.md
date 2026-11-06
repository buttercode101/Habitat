# Responsive Compatibility Report — Habitat

Date: 2026-11-06 · Env: Termux + CI (Playwright not used; Next.js web tier).

## Verified
- Live `https://habitat-za.vercel.app/` 200; `/dashboard` 200; `/evidence` is the correct route (paths probed).
- Web unit test 1/1 pass (`npm test` in `web/`); CI `web-build` green at HEAD.

## Not verified (BLOCKED / NOT VERIFIED)
- 11-viewport matrix, portrait/landscape, zoom/large-text: NOT VERIFIED headlessly in this pass. No Playwright run on Termux.
- Physical-device tests: BLOCKED — no device access.
- iOS Safari / Samsung Internet / Edge / macOS Safari: NOT VERIFIED.

## Recommendation
Add a Playwright matrix for `/`, `/dashboard`, `/evidence`, `/claims/[id]` before any responsive claim. The dashboard is a presentation tier — a broken mobile dashboard would undermine the product's credibility even though the core is a CLI/library.
