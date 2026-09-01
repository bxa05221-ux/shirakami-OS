"""MTM compatibility boundary for protocol normalization.

MTM is intentionally an adapter boundary, not a replacement for existing
protocol loaders. Existing protocol-specific parsers remain authoritative;
this module only normalizes their already-parsed representations into a
stable envelope for the Runtime.
"""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class MTMProtocol:
    """Backend-neutral protocol envelope consumed by Runtime integration."""

    protocol_id: str
    version: str
    name: str
    source_format: str
    payload: Mapping[str, Any]


def normalize(protocol: Any, *, source_format: str = "unknown") -> MTMProtocol:
    """Normalize a parsed protocol without changing its semantics.

    The adapter deliberately accepts arbitrary parsed protocol objects. It
    extracts only stable identity fields and preserves the original parsed
    payload instead of rewriting domain meaning.
    """
    protocol_id = _field(protocol, "protocol_id")
    version = _field(protocol, "version")
    name = _field(protocol, "name", "title")

    if not protocol_id:
        raise ValueError("protocol_id is required")
    if not version:
        raise ValueError("protocol version is required")
    if not name:
        raise ValueError("protocol name/title is required")

    payload = _payload(protocol)
    return MTMProtocol(
        protocol_id=str(protocol_id),
        version=str(version),
        name=str(name),
        source_format=source_format,
        payload=payload,
    )


def _field(value: Any, *names: str) -> Any:
    for name in names:
        if isinstance(value, Mapping) and name in value:
            return value[name]
        if hasattr(value, name):
            return getattr(value, name)
    return None


def _payload(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    if hasattr(value, "__dataclass_fields__"):
        return {name: getattr(value, name) for name in value.__dataclass_fields__}
    if hasattr(value, "__dict__"):
        return dict(vars(value))
    raise TypeError("protocol must be a mapping or parsed object")
