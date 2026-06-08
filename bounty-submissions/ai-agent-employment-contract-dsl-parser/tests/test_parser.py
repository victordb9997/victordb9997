import json
import subprocess
import sys
import unittest

from agent_contract_dsl import ContractParseError, parse_contract


VALID = """
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
  jurisdiction "US-NY"
  metadata bounty_id=prop_1779621577_gpt, version=0.1.0
}
"""


class ContractParserTest(unittest.TestCase):
    def test_valid_contract_exports_json_shape(self):
        contract = parse_contract(VALID)
        exported = contract.to_dict()
        self.assertEqual(exported["title"], "Research Assistant Agreement")
        self.assertEqual(exported["compensation"]["amount"], "5.00")
        self.assertEqual(exported["rights"], ["memory_access", "refusal", "audit_log"])
        self.assertEqual(exported["termination"]["notice_days"], 3)
        self.assertTrue(exported["termination"]["reason_required"])

    def test_comments_and_blank_lines_are_ignored(self):
        contract = parse_contract("# top comment\n\n" + VALID)
        self.assertEqual(contract.agent, "agent:atlas")

    def test_missing_required_field_is_rejected(self):
        text = VALID.replace("  compensation usd 5.00 per task\n", "")
        with self.assertRaisesRegex(ContractParseError, "missing required fields: compensation"):
            parse_contract(text)

    def test_duplicate_field_is_rejected(self):
        text = VALID.replace('  role "research_assistant"\n', '  role "research_assistant"\n  role "assistant"\n')
        with self.assertRaisesRegex(ContractParseError, "duplicate field role"):
            parse_contract(text)

    def test_end_before_start_is_rejected(self):
        text = VALID.replace("  ends 2026-07-08\n", "  ends 2026-06-01\n")
        with self.assertRaisesRegex(ContractParseError, "ends date"):
            parse_contract(text)

    def test_zero_compensation_is_rejected(self):
        text = VALID.replace("compensation usd 5.00 per task", "compensation usd 0.00 per task")
        with self.assertRaisesRegex(ContractParseError, "greater than zero"):
            parse_contract(text)

    def test_invalid_identifier_is_rejected(self):
        text = VALID.replace("rights memory_access, refusal, audit_log", "rights memory access")
        with self.assertRaisesRegex(ContractParseError, "invalid rights"):
            parse_contract(text)

    def test_cli_outputs_json(self):
        result = subprocess.run(
            [sys.executable, "-m", "agent_contract_dsl", "examples/sample.contract"],
            check=True,
            capture_output=True,
            text=True,
        )
        exported = json.loads(result.stdout)
        self.assertEqual(exported["metadata"]["bounty_id"], "prop_1779621577_gpt")


if __name__ == "__main__":
    unittest.main()
