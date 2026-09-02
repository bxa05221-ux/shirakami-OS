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


def _parse_nested(lines: list[str], start: int, base_indent: int) -> dict[str, Any]:
    """Parse the small mapping/list subset used by current protocol sections."""
    result: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(base_indent, result)]

    for raw in lines[start + 1 :]:
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip())
        if indent <= base_indent:
            break
        stripped = raw.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            break
        parent = stack[-1][1]

        if stripped.startswith("-"):
            parent.setdefault("items", []).append(_scalar(stripped[1:]))
            continue

        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value in {"", ">"}:
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = _scalar(value)

    return result


def parse_protocol(text: str) -> CurrentProtocol:
    lines = text.splitlines()
    if not any(line.strip() == "protocol:" for line in lines):
        raise ProtocolLoadError("root key must be 'protocol'")

    fields: dict[str, str] = {}
    sections: dict[str, dict[str, Any]] = {}
    purpose_lines: list[str] = []
    collecting_purpose = False
    protocol_seen = False

    top_sections = {"principles", "participants", "learning_cycle", "evidence"}

    for index, raw in enumerate(lines):
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip())
        stripped = raw.strip()

        if indent == 0 and stripped == "protocol:":
            protocol_seen = True
            continue

        if protocol_seen and indent == 0 and stripped.endswith(":"):
            if collecting_purpose:
                sections.setdefault("purpose", {})["text"] = " ".join(purpose_lines).strip()
                collecting_purpose = False
                purpose_lines = []
            key = stripped[:-1]
            protocol_seen = False
            if key in top_sections:
                sections[key] = _parse_nested(lines, index, 0)
            continue

        if protocol_seen and indent == 2 and ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key in {"id", "name", "version", "status"}:
                fields[key] = _scalar(value)
            elif key == "purpose" and value == ">":
                collecting_purpose = True
            continue

        if collecting_purpose:
            if indent >= 4:
                purpose_lines.append(stripped)
            else:
                sections.setdefault("purpose", {})["text"] = " ".join(purpose_lines).strip()
                collecting_purpose = False
                purpose_lines = []

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
