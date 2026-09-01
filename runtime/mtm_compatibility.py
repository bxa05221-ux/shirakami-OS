"""MTM compatibility boundary for protocol normalization.

MTM does not replace existing protocol loaders. It provides a small, stable
boundary that can carry different protocol representations into Runtime.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from .protocol_loader import ProtocolIR


@dataclass(frozen=True)
class MTMProtocol:
    """Normalized protocol envelope passed across the compatibility boundary."""

    source_format: str
    payload: Mapping[str, Any]


def normalize_protocol(protocol: ProtocolIR | Mapping[str, Any]) -> MTMProtocol:
    """Normalize an existing protocol representation without rewriting it."""
    if isinstance(protocol, ProtocolIR):
        payload = {
            "protocol_id": protocol.protocol_id,
            "title": protocol.title,
            "version": protocol.version,
            "statement": protocol.statement,
            "pipeline": tuple(dict(item) for item in protocol.pipeline),
        }
        return MTMProtocol(source_format="matome-ir", payload=payload)

    if isinstance(protocol, Mapping):
        return MTMProtocol(source_format="mapping", payload=dict(protocol))

    raise TypeError("unsupported protocol representation")
