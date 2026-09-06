"""Crystallize a stabilized Matome YAML flow into a temporary Protocol."""

from __future__ import annotations

import hashlib

from .protocol_loader import ProtocolLoadError, parse_matome
from .protocol_registry import ProtocolRegistry, RegistryEntry


def temporary_protocol_id(matome_yaml: str) -> str:
    """Return a deterministic identifier derived from exact Matome YAML bytes."""
    digest = hashlib.sha256(matome_yaml.encode("utf-8")).hexdigest()[:16]
    return f"matome.temporary.{digest}"


def crystallize_temporary_protocol(
    registry: ProtocolRegistry,
    matome_yaml: str,
) -> RegistryEntry:
    """Parse a stabilized Matome flow and register it as a temporary Protocol."""
    try:
        artifact = parse_matome(matome_yaml)
    except ProtocolLoadError as exc:
        raise ValueError(str(exc)) from exc

    protocol_id = temporary_protocol_id(matome_yaml)
    return registry.register_temporary(protocol_id, artifact)
