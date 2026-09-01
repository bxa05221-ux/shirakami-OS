"""Minimal Runtime bridge for MTM-normalized protocols.

The bridge deliberately does not interpret protocol meaning. It only exposes
an immutable snapshot suitable for the existing Runtime boundary.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from .mtm_compatibility import MTMProtocol, normalize_protocol


@dataclass(frozen=True)
class RuntimeProtocol:
    """Protocol snapshot accepted by the Runtime boundary."""

    protocol_id: str
    version: str
    payload: Mapping[str, Any]


def prepare_runtime_protocol(protocol: MTMProtocol | Any) -> RuntimeProtocol:
    """Prepare an MTM protocol for Runtime without changing its payload."""
    normalized = protocol if isinstance(protocol, MTMProtocol) else normalize_protocol(protocol)
    payload = dict(normalized.payload)

    protocol_id = payload.get("protocol_id")
    version = payload.get("version")
    if not isinstance(protocol_id, str) or not protocol_id:
        raise ValueError("MTM protocol requires protocol_id")
    if not isinstance(version, str) or not version:
        raise ValueError("MTM protocol requires version")

    return RuntimeProtocol(
        protocol_id=protocol_id,
        version=version,
        payload=payload,
    )
