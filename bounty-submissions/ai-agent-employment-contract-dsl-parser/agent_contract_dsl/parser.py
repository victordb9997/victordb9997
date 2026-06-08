from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
import re
from typing import Any


IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9_.:-]+$")
CONTRACT_RE = re.compile(r'^contract\s+"([^"]+)"\s*\{$')
QUOTED_FIELD_RE = re.compile(r'^(agent|employer|role|jurisdiction)\s+"([^"]+)"$')
DATE_FIELD_RE = re.compile(r"^(starts|ends)\s+(\d{4}-\d{2}-\d{2})$")
COMPENSATION_RE = re.compile(r"^compensation\s+([A-Za-z]{3,8})\s+([0-9]+(?:\.[0-9]{1,8})?)\s+per\s+([A-Za-z0-9_.:-]+)$")
LIST_FIELD_RE = re.compile(r"^(rights|obligations)\s+(.+)$")
TERMINATION_RE = re.compile(r"^termination\s+notice_days\s+([0-9]+)\s+reason_required\s+(true|false)$")
METADATA_RE = re.compile(r"^metadata\s+(.+)$")


class ContractParseError(ValueError):
    """Raised when a contract DSL document is malformed."""


@dataclass(frozen=True)
class Compensation:
    currency: str
    amount: Decimal
    cadence: str

    def to_dict(self) -> dict[str, str]:
        return {
            "currency": self.currency,
            "amount": format(self.amount, "f"),
            "cadence": self.cadence,
        }


@dataclass(frozen=True)
class Termination:
    notice_days: int
    reason_required: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "notice_days": self.notice_days,
            "reason_required": self.reason_required,
        }


@dataclass(frozen=True)
class Contract:
    title: str
    agent: str
    employer: str
    role: str
    starts: date
    compensation: Compensation
    rights: list[str]
    obligations: list[str]
    termination: Termination
    ends: date | None = None
    jurisdiction: str | None = None
    metadata: dict[str, str] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "agent": self.agent,
            "employer": self.employer,
            "role": self.role,
            "starts": self.starts.isoformat(),
            "ends": self.ends.isoformat() if self.ends else None,
            "compensation": self.compensation.to_dict(),
            "rights": list(self.rights),
            "obligations": list(self.obligations),
            "termination": self.termination.to_dict(),
            "jurisdiction": self.jurisdiction,
            "metadata": dict(self.metadata or {}),
        }


def parse_contract(text: str) -> Contract:
    lines = _prepare_lines(text)
    if len(lines) < 3:
        raise ContractParseError("contract must include header, body, and closing brace")

    header_line, header = lines[0]
    match = CONTRACT_RE.match(header)
    if not match:
        raise ContractParseError(f"line {header_line}: expected contract header")
    title = match.group(1)

    closing_line, closing = lines[-1]
    if closing != "}":
        raise ContractParseError(f"line {closing_line}: expected closing brace")

    fields: dict[str, Any] = {}
    for line_number, line in lines[1:-1]:
        _parse_body_line(fields, line, line_number)

    required = [
        "agent",
        "employer",
        "role",
        "starts",
        "compensation",
        "rights",
        "obligations",
        "termination",
    ]
    missing = [name for name in required if name not in fields]
    if missing:
        raise ContractParseError(f"missing required fields: {', '.join(missing)}")

    if fields.get("ends") and fields["ends"] < fields["starts"]:
        raise ContractParseError("ends date must not be earlier than starts date")

    return Contract(
        title=title,
        agent=fields["agent"],
        employer=fields["employer"],
        role=fields["role"],
        starts=fields["starts"],
        ends=fields.get("ends"),
        compensation=fields["compensation"],
        rights=fields["rights"],
        obligations=fields["obligations"],
        termination=fields["termination"],
        jurisdiction=fields.get("jurisdiction"),
        metadata=fields.get("metadata", {}),
    )


def _parse_body_line(fields: dict[str, Any], line: str, line_number: int) -> None:
    quoted = QUOTED_FIELD_RE.match(line)
    if quoted:
        _set_once(fields, quoted.group(1), quoted.group(2), line_number)
        return

    dated = DATE_FIELD_RE.match(line)
    if dated:
        _set_once(fields, dated.group(1), _parse_date(dated.group(2), line_number), line_number)
        return

    compensation = COMPENSATION_RE.match(line)
    if compensation:
        currency, amount_text, cadence = compensation.groups()
        _validate_identifier(cadence, line_number, "compensation cadence")
        try:
            amount = Decimal(amount_text)
        except InvalidOperation as exc:
            raise ContractParseError(f"line {line_number}: invalid compensation amount") from exc
        if amount <= 0:
            raise ContractParseError(f"line {line_number}: compensation amount must be greater than zero")
        _set_once(fields, "compensation", Compensation(currency.lower(), amount, cadence), line_number)
        return

    listed = LIST_FIELD_RE.match(line)
    if listed:
        name, body = listed.groups()
        _set_once(fields, name, _parse_identifier_list(body, line_number, name), line_number)
        return

    termination = TERMINATION_RE.match(line)
    if termination:
        notice_days, reason_required = termination.groups()
        _set_once(fields, "termination", Termination(int(notice_days), reason_required == "true"), line_number)
        return

    metadata = METADATA_RE.match(line)
    if metadata:
        _set_once(fields, "metadata", _parse_metadata(metadata.group(1), line_number), line_number)
        return

    raise ContractParseError(f"line {line_number}: unrecognized field")


def _prepare_lines(text: str) -> list[tuple[int, str]]:
    prepared: list[tuple[int, str]] = []
    for number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.split("#", 1)[0].strip()
        if line:
            prepared.append((number, line))
    return prepared


def _set_once(fields: dict[str, Any], name: str, value: Any, line_number: int) -> None:
    if name in fields:
        raise ContractParseError(f"line {line_number}: duplicate field {name}")
    fields[name] = value


def _parse_date(value: str, line_number: int) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ContractParseError(f"line {line_number}: invalid ISO date") from exc


def _parse_identifier_list(body: str, line_number: int, field_name: str) -> list[str]:
    values = [item.strip() for item in body.split(",")]
    if not values or any(not item for item in values):
        raise ContractParseError(f"line {line_number}: {field_name} must contain identifiers")
    for value in values:
        _validate_identifier(value, line_number, field_name)
    return values


def _parse_metadata(body: str, line_number: int) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in [part.strip() for part in body.split(",")]:
        if "=" not in item:
            raise ContractParseError(f"line {line_number}: metadata entries must be key=value")
        key, value = [part.strip() for part in item.split("=", 1)]
        _validate_identifier(key, line_number, "metadata key")
        if not value:
            raise ContractParseError(f"line {line_number}: metadata value cannot be empty")
        result[key] = value
    return result


def _validate_identifier(value: str, line_number: int, field_name: str) -> None:
    if not IDENTIFIER_RE.match(value):
        raise ContractParseError(f"line {line_number}: invalid {field_name} identifier {value!r}")
