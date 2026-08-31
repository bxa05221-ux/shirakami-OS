"""Dependency-free loader for the repository's current ``protocol:`` YAML shape."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .protocol_loader import ProtocolLoadError


@dataclass(frozen=True)
class CurrentProtocol:
    protocol_id: str
    name: str
    version: str
    status: str
    purpose: Mapping[str, Any]
    principles: Mapping[str, Any]
    participants: Mapping[str, Any]
    learning_cycle: Mapping[str, Any]
    evidence: Mapping[str, Any]


def _scalar(value: str) -> str:
    return value.strip().strip('"\'')


def parse_protocol(text: str) -> CurrentProtocol:
    lines = text.splitlines()
    fields: dict[str, str] = {}
    sections: dict[str, dict[str, Any]] = {}

    protocol_seen = False
    current_top: str | None = None
    purpose_lines: list[str] = []
    collecting_purpose = False

    for raw in lines:
        if not raw.strip():
            continue

        indent = len(raw) - len(raw.lstrip())
        stripped = raw.strip()

        # A top-level key closes any active block.
        if indent == 0 and stripped.endswith(":"):
            if collecting_purpose:
                sections.setdefault("purpose", {})["text"] = " ".join(purpose_lines).strip()
                collecting_purpose = False
                purpose_lines = []
            current_top = stripped[:-1]
            if current_top == "protocol":
                protocol_seen = True
            else:
                sections.setdefault(current_top, {})
            continue

        if not protocol_seen:
            continue

        # Fields directly under protocol.
        if current_top == "protocol" and indent == 2 and ":" in stripped:
            if collecting_purpose:
                sections.setdefault("purpose", {})["text"] = " ".join(purpose_lines).strip()
                collecting_purpose = False
                purpose_lines = []

            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key in {"id", "name", "version", "status"}:
                fields[key] = _scalar(value)
            elif key == "purpose" and value == ">":
                collecting_purpose = True
            continue

        if collecting_purpose:
            # purpose is a YAML folded block indented beneath protocol.purpose.
            if indent >= 4:
                purpose_lines.append(stripped)
                continue
            sections.setdefault("purpose", {})["text"] = " ".join(purpose_lines).strip()
            collecting_purpose = False
            purpose_lines = []

        if current_top in {"principles", "participants", "learning_cycle", "evidence"}:
            section = sections.setdefault(current_top, {})
            if indent == 2 and stripped.startswith("-"):
                section.setdefault("items", []).append(_scalar(stripped[1:]))
            elif indent == 2 and ":" in stripped:
                key, value = stripped.split(":", 1)
                if value.strip() not in {"", ">"}:
                    section[key.strip()] = _scalar(value)

    if collecting_purpose:
        sections.setdefault("purpose", {})["text"] = " ".join(purpose_lines).strip()

    missing = [key for key in ("id", "name", "version", "status") if not fields.get(key)]
    if missing:
        raise ProtocolLoadError(f"missing protocol fields: {', '.join(missing)}")
    if not sections.get("purpose", {}).get("text"):
        raise ProtocolLoadError("missing protocol.purpose")

    return CurrentProtocol(
        protocol_id=fields["id"],
        name=fields["name"],
        version=fields["version"],
        status=fields["status"],
        purpose=sections.get("purpose", {}),
        principles=sections.get("principles", {}),
        participants=sections.get("participants", {}),
        learning_cycle=sections.get("learning_cycle", {}),
        evidence=sections.get("evidence", {}),
    )
