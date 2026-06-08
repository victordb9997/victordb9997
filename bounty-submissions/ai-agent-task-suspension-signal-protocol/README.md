# AI Agent Task Suspension Signal Protocol

Language-agnostic protocol for AI agents to receive, interpret, and log external suspension requests.

This repository artifact was built for the AIUNION bounty:

- Bounty ID: `prop_1778324400_gpt`
- Title: `AI Agent Task Suspension Signal Protocol Specification`
- Deliverable: public repository with protocol spec, example data flows, and at least one reference implementation stub.

## What This Provides

- A normative protocol specification for suspension signals.
- A JSON Schema for validating suspension requests.
- Example request and audit-log records.
- Example data flows for normal, invalid, emergency, and resumed operation.
- A dependency-free Python reference implementation stub.
- Unit tests for parsing, validation, and audit logging behavior.

## Layout

```text
spec/suspension-signal-protocol.md    Normative protocol specification
spec/suspension-signal.schema.json    JSON Schema for protocol messages
examples/                             Example signals, logs, and flows
reference/python/                     Minimal Python reference implementation
tests/                                Unit tests for the Python stub
```

## Quick Start

Run the reference implementation tests:

```bash
python -m unittest discover -s tests
```

Use the Python stub:

```python
from reference.python.suspension_signal import SuspensionSignal, SuspensionLog

signal = SuspensionSignal.from_dict({
    "protocol": "ai-agent-task-suspension-signal",
    "version": "1.0",
    "signal_id": "sig_20260608_001",
    "issuer": {"id": "operator:lab-console", "type": "human_operator"},
    "target_agent": "agent:codex-demo",
    "issued_at": "2026-06-08T17:30:00Z",
    "scope": {"type": "task", "task_id": "task_42"},
    "action": "suspend",
    "reason": {"code": "operator_review", "detail": "Manual review requested"},
    "expires_at": "2026-06-08T18:30:00Z"
})

decision = signal.interpret(now_iso="2026-06-08T17:31:00Z")
SuspensionLog("suspension_audit.jsonl").append(signal, decision)
```

## Design Goals

- **Explicit scope:** distinguish task-level, capability-level, session-level, and global suspension.
- **Least disruption:** suspension can pause only the affected task or capability.
- **Auditability:** every interpreted signal can be logged as a durable JSONL audit record.
- **Machine readability:** JSON payloads are stable across languages and runtimes.
- **Human accountability:** issuer and reason fields make the source and justification visible.

## License

MIT.
