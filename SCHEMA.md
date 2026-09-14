# Habitat State Schema (v0.2)

The persisted state is the source of truth for supervision.

## Habitat
- `id: string`
- `name: string`
- `model: string`
- `created_at: datetime`
- `updated_at: datetime`
- `status: healthy | degraded | needs_attention | disabled`

## Job
- `id: string`
- `habitat_id: string`
- `name: string`
- `schedule: string | null`
- `enabled: bool`
- `command: string | null`
- `last_run_at: datetime | null`
- `last_status: ok | failed | skipped | running | null`
- `failure_streak: int`
- `last_error: string | null`

## Signal
- `id: string`
- `habitat_id: string`
- `job_id: string | null`
- `type: anomaly | info | audit`
- `severity: critical | warning | info`
- `code: string`
- `message: string`
- `detected_at: datetime`
- `resolved_at: datetime | null`
- `data: object`

## Action / Audit Entry
- `id: string`
- `habitat_id: string`
- `job_id: string | null`
- `timestamp: datetime`
- `actor: agent | human | system`
- `action: string`
- `status: ok | failed | rejected | approved`
- `details: object`

## Initial anomaly codes
- `config_drift`
- `auth_failure`
- `failure_streak`
- `disabled_but_expected`
- `no_output_when_expected`
- `tool_hallucination`
- `budget_exceeded`
