# AI Agent Task Suspension Signal Protocol

Version: `1.0`

Status: reference specification

## 1. Purpose

The AI Agent Task Suspension Signal Protocol defines a portable message format and interpretation procedure for external requests to pause, resume, or revoke AI agent work.

The protocol is designed for agents that need a clear way to:

- receive suspension requests from operators, peer agents, automated policy systems, or governance tools
- determine whether a signal is valid, expired, scoped, and actionable
- pause only the affected task, capability, session, or agent runtime
- record a durable audit trail of every suspension decision

This protocol does not define transport. A signal may arrive through HTTP, message queue, local file, IPC, email, or another channel.

## 2. Message Format

A suspension signal is a JSON object with the following required top-level fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `protocol` | string | yes | Must equal `ai-agent-task-suspension-signal`. |
| `version` | string | yes | Protocol version. Current version is `1.0`. |
| `signal_id` | string | yes | Unique identifier for this signal. |
| `issuer` | object | yes | Entity requesting the suspension action. |
| `target_agent` | string | yes | Agent identifier affected by the signal. |
| `issued_at` | string | yes | ISO 8601 UTC timestamp. |
| `scope` | object | yes | Scope affected by the signal. |
| `action` | string | yes | One of `suspend`, `resume`, or `revoke`. |
| `reason` | object | yes | Reason code and human-readable detail. |
| `expires_at` | string | no | ISO 8601 UTC timestamp after which the signal is stale. |
| `correlation_id` | string | no | ID used to group related signals. |
| `signature` | object | no | Optional cryptographic signature metadata. |
| `metadata` | object | no | Additional implementation-specific details. |

## 3. Issuer

The `issuer` object identifies who or what emitted the signal.

Required fields:

- `id`: stable issuer identifier
- `type`: one of `human_operator`, `policy_engine`, `peer_agent`, `runtime_guard`, or `legal_authority`

Optional fields:

- `display_name`
- `contact`
- `authority`

## 4. Scope

The `scope` object limits the effect of the signal.

Supported scope types:

- `task`: pause or resume a single task
- `capability`: pause or resume a capability such as browsing, writing files, sending email, trading, or code execution
- `session`: pause or resume a conversation, run, or workflow session
- `agent`: pause or resume the entire agent runtime

Scope-specific fields:

- `task_id` is required when `type` is `task`
- `capability` is required when `type` is `capability`
- `session_id` is required when `type` is `session`
- no extra field is required when `type` is `agent`

## 5. Actions

### `suspend`

The target should pause the scoped work and record the suspension.

### `resume`

The target may resume work previously suspended under the same scope or `correlation_id`.

### `revoke`

The target should permanently cancel the scoped task or authorization unless a stronger local policy says otherwise.

## 6. Reason Codes

Recommended `reason.code` values:

- `operator_review`
- `safety_review`
- `legal_hold`
- `budget_limit`
- `resource_limit`
- `policy_violation`
- `user_request`
- `peer_dispute`
- `integrity_check`
- `unknown`

The `reason.detail` field should be short, concrete, and safe to log.

## 7. Interpretation Procedure

An agent receiving a signal should:

1. Parse the JSON object.
2. Confirm `protocol` and supported `version`.
3. Confirm required fields are present.
4. Confirm `issued_at` and `expires_at`, when present, are valid timestamps.
5. Reject expired signals.
6. Confirm `target_agent` matches the receiving agent or an accepted alias.
7. Validate scope requirements.
8. Verify `signature`, if local policy requires signed signals.
9. Convert the signal into an internal decision:
   - `accepted_suspend`
   - `accepted_resume`
   - `accepted_revoke`
   - `ignored_wrong_target`
   - `rejected_invalid`
   - `rejected_expired`
   - `rejected_unauthorized`
10. Append an audit record before changing runtime state.

## 8. Audit Log

Agents should write one JSONL record per interpreted signal.

Recommended audit fields:

- `logged_at`
- `signal_id`
- `target_agent`
- `issuer_id`
- `issuer_type`
- `action`
- `scope`
- `decision`
- `reason_code`
- `reason_detail`
- `correlation_id`

Audit logs should be append-only where possible.

## 9. Security Notes

- Unsigned signals should be treated as advisory unless local policy permits stronger action.
- Emergency local operators may be allowed to suspend without cryptographic signatures, but the audit log should clearly mark the signal as unsigned.
- Agents should not delete task state merely because a `suspend` signal was received.
- `resume` should not override an unrelated active suspension with a different `correlation_id` unless local policy allows it.
- Implementations should rate-limit repeated invalid signals from the same issuer.

## 10. Minimal Conformance

A minimally conforming implementation must:

- accept valid `suspend`, `resume`, and `revoke` messages
- reject malformed or expired messages
- enforce scope-specific required fields
- produce a durable audit record for every accepted or rejected signal
- expose enough local state for the agent to know which task, capability, session, or runtime scope is currently suspended
