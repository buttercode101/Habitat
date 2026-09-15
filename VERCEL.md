# Habitat on Vercel

Habitat uses a two-layer deployment model. The persistent Python Habitat service remains the source of truth for SQLite, the ledger, policy evaluation, events, agents, claims and proof generation. Vercel hosts the public inspection UI and a small server-side proxy that keeps the Habitat bearer token off the browser.

The existing SQLite-backed HTTP service is intentionally not moved into a Vercel serverless function. Vercel is the presentation/API edge; the durable Habitat process belongs on a persistent service.

## Vercel project

When importing `buttercode101/Habitat` from Git:

1. Select the repository.
2. Set **Root Directory** to `web`.
3. Framework preset: **Next.js**.
4. Build command: `next build`.
5. Add these server-only environment variables for Preview and Production:
   - `HABITAT_API_URL` — HTTPS URL of the persistent Habitat service.
   - `HABITAT_API_TOKEN` — the Habitat server bearer secret.
6. Do **not** prefix the token with `NEXT_PUBLIC_`.
7. Deploy.

The web package uses the current Next.js 16.3.x line. Do not pin the new Vercel surface back to the older 15.5.7 package that was initially scaffolded.

## Habitat backend

The backend must be reachable by the Vercel deployment over HTTPS. Run the existing Habitat service on a persistent host with:

```bash
habitat serve --host 0.0.0.0 --port 8787 --secret-env HABITAT_SERVER_SECRET
```

Use a strong random `HABITAT_SERVER_SECRET`. Put TLS in front of the service and restrict the backend to the minimum network surface required by the Vercel proxy. Do not put the SQLite database on an ephemeral filesystem.

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

## Important boundary

This does **not** make Habitat's SQLite-backed service serverless. It deliberately keeps the durable protocol state in one persistent service and makes Vercel the presentation/API edge. If the backend is unavailable, the Vercel UI shows a connection error rather than fabricating status or metrics.
