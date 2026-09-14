# Agent identity

Habitat treats **identity**, **authorization**, and **cryptographic trust** as separate controls.

- **Identity:** who an agent is (`agent_id`).
- **Authorization:** what that identity is allowed to submit/do.
- **Trust:** which signing key is accepted for that identity.

## Lifecycle

`active → disabled → active` is allowed.

`active/disabled → revoked` is terminal. A revoked identity cannot be re-enabled; create a new identity instead. This prevents an old credential from silently regaining authority after revocation.

## Key binding

A `TrustedKey` may be bound to an `agent_id`. When bound, a valid signature from that key is trusted only for that agent. Key expiry and revocation remain independent controls.

## Security boundary

Identity does not prove that an agent behaved correctly. It only establishes an actor namespace. Habitat still requires the evidence, integrity, policy, and (where configured) signature checks needed for a claim verdict.
