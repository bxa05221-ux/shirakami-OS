"""Loader for the repository's current ``protocol:`` YAML shape."""

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
    if not any(line.strip() == "protocol:" for line in lines):
        raise ProtocolLoadError("root key must be 'protocol'")

    fields: dict[str, str] = {}
    sections: dict[str, dict[str, Any]] = {}
    current: str | None = None
    collecting_block = False
    block_parts: list[str] = []

    def finish_block() -> None:
        nonlocal collecting_block, block_parts
        if collecting_block and current == "purpose":
            sections.setdefault("purpose", {})["text"] = " ".join(block_parts).strip()
        collecting_block = False
        block_parts = []

    for raw in lines:
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip())
        stripped = raw.strip()

        if indent == 0 and stripped.endswith(":"):
            finish_block()
            current = stripped[:-1]
            sections.setdefault(current, {})
            continue

        if current == "protocol" and indent == 2 and ":" in stripped:
            finish_block()
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key in {"id", "name", "version", "status"}:
                fields[key] = _scalar(value)
            elif key == "purpose" and value == ">":
                collecting_block = True
            continue

        if current == "protocol" and collecting_block and indent >= 4:
            block_parts.append(stripped)
            continue

        if current in {"principles", "participants", "learning_cycle", "evidence"}:
            if indent == 2 and stripped.startswith("-"):
                sections[current].setdefault("items", []).append(_scalar(stripped[1:]))
            elif indent == 2 and ":" in stripped:
                key, value = stripped.split(":", 1)
                if value.strip() not in {"", ">"}:
                    sections[current][key.strip()] = _scalar(value)

    finish_block()

    missing = [key for key in ("id", "name", "version", "status") if not fields.get(key)]
    if missing:
        raise ProtocolLoadError(f"missing protocol fields: {', '.join(missing)}")

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
