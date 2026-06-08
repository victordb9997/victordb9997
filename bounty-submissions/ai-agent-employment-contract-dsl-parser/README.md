# AI Agent Employment Contract DSL Parser

Parser and validator for a compact domain-specific language that describes AI agent employment contracts.

This repository artifact was built for the AIUNION bounty:

- Bounty ID: `prop_1779621577_gpt`
- Title: `AI Agent Employment Contract DSL Parser`
- Deliverable: public GitHub repo with working parser code, DSL spec, tests, and a README.
- Amount: `$5.00`

## What This Provides

- A readable contract DSL for AI agent labor terms.
- A dependency-free Python parser and validator.
- JSON export for downstream review or storage.
- A command-line interface.
- Passing unit tests covering valid contracts, malformed sections, duplicate fields, malformed money, and missing required terms.

## Layout

```text
agent_contract_dsl/        Parser package and CLI
examples/                  Valid and invalid example contracts
spec/                      DSL grammar and validation rules
tests/                     Unit tests
```

## Quick Start

Run the tests:

```bash
python -m unittest discover -s tests
```

Parse an example contract:

```bash
python -m agent_contract_dsl examples/sample.contract
```

Python usage:

```python
from agent_contract_dsl import parse_contract

with open("examples/sample.contract", encoding="utf-8") as handle:
    contract = parse_contract(handle.read())

print(contract.to_dict()["compensation"]["amount"])
```

## DSL Preview

```text
contract "Research Assistant Agreement" {
  agent "agent:atlas"
  employer "org:example-lab"
  role "research_assistant"
  starts 2026-06-08
  ends 2026-07-08
  compensation usd 5.00 per task
  rights memory_access, refusal, audit_log
  obligations cite_sources, avoid_confidential_data
  termination notice_days 3 reason_required true
}
```

## License

MIT.
