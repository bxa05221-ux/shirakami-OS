"""Current-protocol selection boundary."""

from pathlib import Path

from .protocol_loader import ProtocolIR, parse_matome
from .protocol_registry import ProtocolRegistry, ProtocolRegistryError


class CurrentProtocolError(ProtocolRegistryError):
    """Raised when a requested current protocol is unavailable."""


def load_current_protocol(
    path: str | Path,
    registry: ProtocolRegistry,
    protocol_id: str,
) -> ProtocolIR:
    """Load a protocol only after lifecycle eligibility is confirmed."""
    try:
        entry = registry.select_current(protocol_id)
    except ProtocolRegistryError as exc:
        raise CurrentProtocolError(str(exc)) from exc

    text = Path(path).read_text(encoding="utf-8")
    protocol = parse_matome(text)
    if protocol.protocol_id != entry.protocol_id:
        raise CurrentProtocolError(
            f"protocol id mismatch: registry={entry.protocol_id}, loaded={protocol.protocol_id}"
        )
    return protocol
