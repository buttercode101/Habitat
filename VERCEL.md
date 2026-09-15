# Habitat on Vercel

Habitat uses a two-layer deployment model. The persistent Python Habitat service remains the source of truth for SQLite, the ledger, policy evaluation, events, agents, claims and proof generation. Vercel hosts the inspection UI and a small server-side proxy that keeps the Habitat bearer token off the browser.

The existing SQLite-backed HTTP service is intentionally not moved into a Vercel serverless function. Vercel is the presentation/API edge; the durable Habitat process belongs on a persistent service.

## Vercel project

When importing `buttercode101/Habitat` from Git:

1. Select the repository.
2. Set **Root Directory** to `web`.
3. Framework preset: **Next.js**.
4. Build command: `npm run build` (the repository also provides `web/vercel.json`).
5. Add these server-only environment variables for Preview and Production:
   - `HABITAT_API_URL` — HTTPS URL of the persistent Habitat service.
   - `HABITAT_API_TOKEN` — the Habitat server bearer secret.
6. Do **not** prefix the token with `NEXT_PUBLIC_`.
7. Deploy.

The web package uses the current Next.js 16.3.x line. Do not pin the Vercel surface back to an older Next.js release.

The deployed inspection surface is intentionally `noindex`/`nofollow`; it is an operational UI, not a marketing site. **This is not authentication.** If claim or evidence data is sensitive, put an authenticated access layer in front of the Vercel deployment or keep the inspection surface private.

## Habitat backend

The backend must be reachable by the Vercel deployment over HTTPS. Run the existing Habitat service on a persistent host with:

```bash
habitat serve --host 0.0.0.0 --port 8787 --secret-env HABITAT_WEBHOOK_SECRET
```

Use a strong random `HABITAT_WEBHOOK_SECRET`. Put TLS in front of the service and restrict the backend to the minimum network surface required by the Vercel proxy. Do not put the SQLite database on an ephemeral filesystem.

The server defaults to requiring signed webhook events. If you deliberately deploy a mode that accepts unsigned events, use `--allow-unsigned` only with an explicit understanding of that trust boundary.

## Request flow

```text
Browser
   │
   ▼
Vercel / Next.js
   │  server-side bearer token
   ▼
Persistent Habitat HTTP service
   │
   ▼
SQLite + ledger + policy + proof
```

The browser never receives `HABITAT_API_TOKEN`. The Vercel layer proxies only the inspection/verification calls needed by the UI.

The Vercel proxy enforces HTTPS for `HABITAT_API_URL` in production and applies a 10-second upstream timeout. Proxy error responses are deliberately generic so backend details are not unnecessarily exposed to public callers.

## Important boundary

This does **not** make Habitat's SQLite-backed service serverless. It deliberately keeps the durable protocol state in one persistent service and makes Vercel the presentation/API edge. If the backend is unavailable, the Vercel UI shows a connection error rather than fabricating status or metrics.
