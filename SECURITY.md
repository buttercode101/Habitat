# Habitat Security Model

## Security goals

Habitat protects the integrity of its local record of configured jobs, trusted actions, authenticated events, claims, and signals.

It does **not** claim to sandbox arbitrary code or make an already-compromised operating system trustworthy.

The action ledger is **tamper-evident**: each recorded action is chained to the previous action with a SHA-256 digest, and claim verification refuses to treat the ledger as trusted when the chain is inconsistent. This detects modification, deletion, insertion, or incomplete ledger state after the integrity chain was established. It is not a remote or independently anchored attestation: an attacker with unrestricted database control could rewrite both the records and integrity metadata.

## Default boundaries

- API binds to `127.0.0.1` by default.
- Signed events are required by default.
- HMAC comparison uses constant-time comparison.
- Events are bounded to 256 KiB.
- Event IDs are persistent and idempotent.
- Agent permissions are explicit and least-privilege by default.
- Network claims tied to jobs require a run/correlation ID.
- SQLite is opened with foreign keys and WAL mode.
- Trusted action verification includes an integrity-chain check.
- Portable proof verification rejects non-finite JSON numbers, timezone-less timestamps, proofs larger than 16 MiB, or ledgers containing more than 10,000 actions.
- HTTP evidence adapters accept only HTTP(S), reject redirects, reject URL credentials, and bound response bodies to 1 MiB.
- Remote server and agent authentication failures are throttled to reduce brute-force and CPU-exhaustion attacks; localhost remains unthrottled.

## Secrets

Do not commit webhook or agent secrets. Prefer environment variables or a secret manager supplied by the deployment environment.

Agent secrets are stored as salted PBKDF2-HMAC-SHA256 hashes with a deliberately high work factor. Databases created by older Habitat versions may contain legacy SHA-256 agent-secret hashes; a successful authentication transparently upgrades that credential to the hardened format.

CLI commands do not accept agent/webhook secrets as direct arguments because command-line arguments can be exposed through shell history, process listings, CI logs, or monitoring. Use `HABITAT_WEBHOOK_SECRET`, `HABITAT_AGENT_SECRET`, or another explicitly configured environment variable instead.

The generated agent secret is displayed once by `agent-add`; store it securely and rotate/disable the agent if it is exposed.

## Threats and controls

| Threat | Control |
|---|---|
| Forged event | HMAC signature |
| Duplicate event after first receipt | Persistent event ID + payload conflict detection |
| Unauthorized agent | Agent identity + permission check + per-agent secret |
| Authentication brute force / PBKDF2 CPU exhaustion | Remote failure throttle; localhost is intentionally trusted local access |
| Stale claim | Run/correlation binding |
| Ambiguous trusted action attribution | Run ID required when more than one correlated action exists |
| Tampered trusted action | Chained action-integrity digest |
| Oversized request | 256 KiB limit |
| Oversized portable proof | 16 MiB file limit + 10,000-action limit |
| Non-standard JSON numbers | Strict JSON constant rejection |
| Malformed payload | Structural validation |
| Arbitrary shell interpretation | `ShellAdapter` uses argv parsing by default |
| Evidence redirect / oversized response | Redirect rejection + 1 MiB response bound |
| Database upgrade breakage | Schema version metadata + backup workflow |
| Evidence mismatch | Typed expected fields / status |

### Replay limitation

Event IDs make retries idempotent **after Habitat has received the event**. They do not provide freshness against an attacker who captures a valid signed event and submits it before the legitimate sender's first delivery. Deployments that require replay resistance at that boundary should add a trusted freshness/nonce mechanism at the transport or agent-enforcement layer rather than treating HMAC alone as proof of freshness.

## Deployment guidance

For a single-user workstation, the default localhost server is appropriate.

For a shared or remote deployment:

1. Keep Habitat behind a TLS-terminating reverse proxy.
2. Restrict network access with firewall rules.
3. Use strong, rotated secrets.
4. Do not enable unsigned events.
5. Run under a dedicated OS account.
6. Give the process the minimum filesystem permissions required.
7. Back up the SQLite database.
8. Treat job commands as privileged configuration.
9. Monitor disk space and log output.
10. Treat exported proof bundles as potentially sensitive because action details and event payloads may contain operational data.

Remote authentication throttling is deliberately in-process and keyed by client address. It is a defense-in-depth control, not a substitute for a reverse proxy, firewall, rate-limiting gateway, or account lockout policy in hostile public deployments.

## Incident response

If an agent secret is suspected to be compromised, disable or replace that agent credential and review the event/action ledger for the affected period. If the action-integrity check fails, treat trusted claims from the affected ledger as **inconclusive** until the record is restored or independently corroborated. Because Habitat is an audit system, do not erase evidence merely to hide the incident.

## Known non-goals

Habitat is not a general sandbox, EDR, SIEM, secrets manager, or multi-tenant SaaS control plane. Those concerns require additional infrastructure when the deployment demands them.
