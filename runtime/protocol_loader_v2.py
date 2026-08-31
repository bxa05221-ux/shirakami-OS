"""Loader for the repository's current ``protocol:`` YAML shape.

This is intentionally a narrow structural loader. It preserves the current
ProtocolIR boundary without changing the β0.1 Matome loader.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .protocol_loader import ProtocolIR, ProtocolLoadError


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
    """Parse the current repository protocol shape using PyYAML."""
    try:
        import yaml
    except ImportError as exc:
        raise ProtocolLoadError("PyYAML is required for current protocol format") from exc

    document = yaml.safe_load(text)
    if not isinstance(document, dict) or not isinstance(document.get("protocol"), dict):
        raise ProtocolLoadError("root key must be 'protocol'")

    protocol = document["protocol"]
    required = ("id", "name", "version", "status")
    missing = [key for key in required if not protocol.get(key)]
    if missing:
        raise ProtocolLoadError(f"missing protocol fields: {', '.join(missing)}")

    return CurrentProtocol(
        protocol_id=str(protocol["id"]),
        name=str(protocol["name"]),
        version=str(protocol["version"]),
        status=str(protocol["status"]),
        purpose=document.get("purpose", {}),
        principles=document.get("principles", {}),
        participants=document.get("participants", {}),
        learning_cycle=document.get("learning_cycle", {}),
        evidence=document.get("evidence", {}),
    )
