from pathlib import Path
import json
import tempfile
import unittest

from reference.python.suspension_signal import (
    SuspensionLog,
    SuspensionSignal,
    SuspensionSignalError,
)


VALID = {
    "protocol": "ai-agent-task-suspension-signal",
    "version": "1.0",
    "signal_id": "sig_001",
    "issuer": {"id": "operator:test", "type": "human_operator"},
    "target_agent": "agent:test",
    "issued_at": "2026-06-08T17:30:00Z",
    "expires_at": "2026-06-08T18:30:00Z",
    "scope": {"type": "task", "task_id": "task_1"},
    "action": "suspend",
    "reason": {"code": "operator_review", "detail": "review requested"},
}


class SuspensionSignalTest(unittest.TestCase):
    def test_valid_suspend_is_accepted(self):
        signal = SuspensionSignal.from_dict(dict(VALID))
        decision = signal.interpret(target_agent="agent:test", now_iso="2026-06-08T17:31:00Z")
        self.assertEqual(decision, "accepted_suspend")

    def test_wrong_target_is_ignored(self):
        signal = SuspensionSignal.from_dict(dict(VALID))
        decision = signal.interpret(target_agent="agent:other", now_iso="2026-06-08T17:31:00Z")
        self.assertEqual(decision, "ignored_wrong_target")

    def test_expired_signal_is_rejected(self):
        signal = SuspensionSignal.from_dict(dict(VALID))
        decision = signal.interpret(target_agent="agent:test", now_iso="2026-06-08T19:31:00Z")
        self.assertEqual(decision, "rejected_expired")

    def test_scope_specific_field_required(self):
        payload = dict(VALID)
        payload["scope"] = {"type": "task"}
        with self.assertRaises(SuspensionSignalError):
            SuspensionSignal.from_dict(payload)

    def test_resume_action(self):
        payload = dict(VALID)
        payload["action"] = "resume"
        signal = SuspensionSignal.from_dict(payload)
        self.assertEqual(signal.interpret(now_iso="2026-06-08T17:31:00Z"), "accepted_resume")

    def test_audit_log_writes_jsonl(self):
        signal = SuspensionSignal.from_dict(dict(VALID))
        decision = signal.interpret(now_iso="2026-06-08T17:31:00Z")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "audit.jsonl"
            record = SuspensionLog(path).append(signal, decision)
            saved = json.loads(path.read_text().strip())
        self.assertEqual(record["decision"], "accepted_suspend")
        self.assertEqual(saved["signal_id"], "sig_001")


if __name__ == "__main__":
    unittest.main()
