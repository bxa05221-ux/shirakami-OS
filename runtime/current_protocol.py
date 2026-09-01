"""Current-protocol selection boundary.

The existing Matome loader remains unchanged. Registry state is applied only
when a caller explicitly asks for a current protocol.
"""

from pathlib import Path
from typing import Any

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
    entry = registry.select_current(protocol_id)
    text = Path(path).read_text(encoding="utf-8")
    protocol = parse_matome(text)
    if protocol.protocol_id != entry.protocol_id:
        raise CurrentProtocolError(
            f"protocol id mismatch: registry={entry.protocol_id}, loaded={protocol.protocol_id}"
        )
    return protocol
