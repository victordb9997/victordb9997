"""Dependency-free reference stub for AI Agent Task Suspension Signal Protocol."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


PROTOCOL = "ai-agent-task-suspension-signal"
SUPPORTED_VERSION = "1.0"
VALID_ACTIONS = {"suspend", "resume", "revoke"}
VALID_ISSUER_TYPES = {
    "human_operator",
    "policy_engine",
    "peer_agent",
    "runtime_guard",
    "legal_authority",
}
REQUIRED_SCOPE_FIELD = {
    "task": "task_id",
    "capability": "capability",
    "session": "session_id",
    "agent": None,
}


class SuspensionSignalError(ValueError):
    """Raised when a suspension signal is malformed."""


def parse_utc(value: str) -> datetime:
    """Parse an ISO 8601 UTC timestamp."""
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise SuspensionSignalError("timestamp must include timezone")
    return parsed.astimezone(timezone.utc)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class SuspensionSignal:
    payload: dict[str, Any]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SuspensionSignal":
        signal = cls(payload=payload)
        signal.validate()
        return signal

    @classmethod
    def from_json(cls, text: str) -> "SuspensionSignal":
        return cls.from_dict(json.loads(text))

    def validate(self) -> None:
        required = [
            "protocol",
            "version",
            "signal_id",
            "issuer",
            "target_agent",
            "issued_at",
            "scope",
            "action",
            "reason",
        ]
        missing = [field for field in required if field not in self.payload]
        if missing:
            raise SuspensionSignalError(f"missing required fields: {', '.join(missing)}")

        if self.payload["protocol"] != PROTOCOL:
            raise SuspensionSignalError("unsupported protocol")
        if self.payload["version"] != SUPPORTED_VERSION:
            raise SuspensionSignalError("unsupported version")
        if self.payload["action"] not in VALID_ACTIONS:
            raise SuspensionSignalError("unsupported action")

        issuer = self.payload["issuer"]
        if not isinstance(issuer, dict) or not issuer.get("id"):
            raise SuspensionSignalError("issuer.id is required")
        if issuer.get("type") not in VALID_ISSUER_TYPES:
            raise SuspensionSignalError("issuer.type is invalid")

        scope = self.payload["scope"]
        if not isinstance(scope, dict):
            raise SuspensionSignalError("scope must be an object")
        scope_type = scope.get("type")
        if scope_type not in REQUIRED_SCOPE_FIELD:
            raise SuspensionSignalError("scope.type is invalid")
        required_scope_field = REQUIRED_SCOPE_FIELD[scope_type]
        if required_scope_field and not scope.get(required_scope_field):
            raise SuspensionSignalError(f"scope.{required_scope_field} is required for {scope_type} scope")

        reason = self.payload["reason"]
        if not isinstance(reason, dict) or not reason.get("code") or not reason.get("detail"):
            raise SuspensionSignalError("reason.code and reason.detail are required")

        parse_utc(self.payload["issued_at"])
        if self.payload.get("expires_at"):
            parse_utc(self.payload["expires_at"])

    def interpret(self, target_agent: str | None = None, now_iso: str | None = None) -> str:
        """Return an interpretation decision for this signal."""
        if target_agent and self.payload["target_agent"] != target_agent:
            return "ignored_wrong_target"

        now = parse_utc(now_iso) if now_iso else datetime.now(timezone.utc)
        expires_at = self.payload.get("expires_at")
        if expires_at and parse_utc(expires_at) < now:
            return "rejected_expired"

        return {
            "suspend": "accepted_suspend",
            "resume": "accepted_resume",
            "revoke": "accepted_revoke",
        }[self.payload["action"]]

    def audit_record(self, decision: str, logged_at: str | None = None) -> dict[str, Any]:
        issuer = self.payload["issuer"]
        reason = self.payload["reason"]
        return {
            "logged_at": logged_at or utc_now_iso(),
            "signal_id": self.payload["signal_id"],
            "target_agent": self.payload["target_agent"],
            "issuer_id": issuer["id"],
            "issuer_type": issuer["type"],
            "action": self.payload["action"],
            "scope": self.payload["scope"],
            "decision": decision,
            "reason_code": reason["code"],
            "reason_detail": reason["detail"],
            "correlation_id": self.payload.get("correlation_id"),
        }


class SuspensionLog:
    """Append-only JSONL audit log writer."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def append(self, signal: SuspensionSignal, decision: str) -> dict[str, Any]:
        record = signal.audit_record(decision)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
        return record
