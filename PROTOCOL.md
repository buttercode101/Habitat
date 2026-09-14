# Habitat Event Protocol v1

Events are JSON objects sent to `POST /v1/events`.

## Required fields

```json
{
  "id": "evt-unique",
  "type": "job.completed",
  "habitat_id": "demo"
}
```

`id` must be unique within the Habitat. Reusing an ID is treated as a duplicate.

## Job events

`job.started`, `job.completed`, and `job.failed` require `job_id` and should include `run_id`.

```json
{
  "id": "evt-123",
  "type": "job.completed",
  "habitat_id": "demo",
  "job_id": "repo-sync",
  "run_id": "run-123",
  "agent_id": "worker-1"
}
```

`job.failed` may include `error`.

## Heartbeats

```json
{
  "id": "evt-heartbeat-1",
  "type": "agent.heartbeat",
  "habitat_id": "demo",
  "agent_id": "worker-1"
}
```

## Claims

Claims tied to a job require `run_id` or `correlation_id` for network submission.

```json
{
  "id": "evt-claim-1",
  "type": "claim.submitted",
  "habitat_id": "demo",
  "job_id": "repo-sync",
  "action": "run_job",
  "run_id": "run-123",
  "claim": "repository synchronization completed",
  "expected_status": "ok"
}
```

## Signing

Sign the exact UTF-8 request body with HMAC-SHA256 using the configured shared secret. Send the lowercase hexadecimal digest in `X-Habitat-Signature`. `sha256=<digest>` is also accepted.

Do not parse and reserialize JSON before signing: the bytes being signed must be the bytes being transmitted.
