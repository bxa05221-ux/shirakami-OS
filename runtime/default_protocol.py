"""Bootstrap the mandatory OS default Protocol."""

from __future__ import annotations

from .protocol_loader import parse_matome
from .protocol_registry import ProtocolRegistry, ProtocolRegistryError, RegistryEntry

DEFAULT_PROTOCOL_YAML = """matome:
  title: Shirakami OS Default Protocol
  version: 0.1
  statement: >
    Provide the permanent runtime footing for registered Protocol requests
    without defining domain-specific interaction semantics.
  pipeline:
    - phase: request_resolution
      action: resolve_protocol_request
    - phase: protocol_execution
      action: execute_protocol
    - phase: evidence_capture
      action: capture_observation
    - phase: observation
      action: observe_landscape
"""

DEFAULT_PROTOCOL_ID = "matome.protocol.default"


def bootstrap_default_protocol(registry: ProtocolRegistry) -> RegistryEntry:
    """Ensure the mandatory default Protocol exists and return it."""
    try:
        return registry.require_default()
    except ProtocolRegistryError:
        artifact = parse_matome(DEFAULT_PROTOCOL_YAML)
        return registry.register_default(DEFAULT_PROTOCOL_ID, artifact)
