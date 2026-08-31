"""Loader for the repository's current ``protocol:`` YAML shape.

This intentionally parses only the current protocol contract needed by the
Runtime boundary. It uses the same dependency-free approach as the β0.1
Matome loader and does not attempt to implement full YAML.
"""

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


def parse_protocol(text: str) -> CurrentProtocol:
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    if not lines or lines[0].strip() != "protocol:":
        raise ProtocolLoadError("root key must be 'protocol'")

    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.startswith("  ") and not line.startswith("    ") and ":" in line:
            key, value = line.strip().split(":", 1)
            if key in {"id", "name", "version", "status"}:
                fields[key] = value.strip().strip('"\'')

    missing = [key for key in ("id", "name", "version", "status") if not fields.get(key)]
    if missing:
        raise ProtocolLoadError(f"missing protocol fields: {', '.join(missing)}")

    sections: dict[str, dict[str, Any]] = {}
    current: str | None = None
    for line in lines[1:]:
        if len(line) == len(line.lstrip()) and line.endswith(":"):
            current = line[:-1]
            if current not in {"protocol"}:
                sections[current] = {}
            continue
        if current in {"purpose", "principles", "participants", "learning_cycle", "evidence"}:
            stripped = line.strip()
            if ":" in stripped:
                key, value = stripped.split(":", 1)
                sections[current][key.strip()] = value.strip().strip('"\'')

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
