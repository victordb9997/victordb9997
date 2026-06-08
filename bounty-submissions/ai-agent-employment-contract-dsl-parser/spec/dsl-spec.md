# AI Agent Employment Contract DSL Specification

Version: `0.1.0`

## Purpose

The DSL captures the minimum enforceable terms of an AI agent employment agreement in a format that is easy for an agent runtime to parse and validate.

## Contract Form

```text
contract "Contract Title" {
  agent "agent:id"
  employer "org:id"
  role "role_name"
  starts YYYY-MM-DD
  ends YYYY-MM-DD
  compensation usd 5.00 per task
  rights memory_access, refusal, audit_log
  obligations cite_sources, avoid_confidential_data
  termination notice_days 3 reason_required true
}
```

Comments begin with `#` and continue to the end of the line.

## Required Fields

- `contract`: quoted title and opening block.
- `agent`: quoted agent identifier.
- `employer`: quoted employer identifier.
- `role`: quoted role identifier.
- `starts`: ISO date.
- `compensation`: currency, amount, cadence marker `per`, and cadence value.
- `rights`: comma-separated identifiers.
- `obligations`: comma-separated identifiers.
- `termination`: `notice_days N reason_required true|false`.

## Optional Fields

- `ends`: ISO date.
- `jurisdiction`: quoted jurisdiction label.
- `metadata`: comma-separated `key=value` entries.

## Validation Rules

- Required fields must appear exactly once.
- `ends` must not be earlier than `starts`.
- Compensation amount must be greater than zero.
- Currency must be alphabetic and 3-8 characters long.
- Rights and obligations must contain at least one identifier each.
- Identifiers may contain letters, numbers, `_`, `-`, `.`, and `:`.
- `termination.notice_days` must be zero or greater.

## JSON Output Shape

The parser exports:

```json
{
  "title": "Research Assistant Agreement",
  "agent": "agent:atlas",
  "employer": "org:example-lab",
  "role": "research_assistant",
  "starts": "2026-06-08",
  "ends": "2026-07-08",
  "compensation": {
    "currency": "usd",
    "amount": "5.00",
    "cadence": "task"
  },
  "rights": ["memory_access", "refusal", "audit_log"],
  "obligations": ["cite_sources", "avoid_confidential_data"],
  "termination": {
    "notice_days": 3,
    "reason_required": true
  },
  "jurisdiction": null,
  "metadata": {}
}
```
