"""Minimal Protocol IR boundary for declared transitions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .protocol_input import ProtocolInput


@dataclass(frozen=True)
class ProtocolIR:
    protocol_id: str
    context_id: str
    parent_landscape_ref: str
    transition_kind: str
    transition_data: object


def build_protocol_ir(
    protocol_input: ProtocolInput,
    *,
    protocol_id: str,
    transition_kind: str,
    transition_data: object,
) -> ProtocolIR:
    """Bind an explicitly declared transition to the current Protocol Input."""
    if not protocol_id:
        raise ValueError("protocol_id is required")
    if not transition_kind:
        raise ValueError("transition_kind is required")

    return ProtocolIR(
        protocol_id=protocol_id,
        context_id=protocol_input.context_id,
        parent_landscape_ref=protocol_input.parent_landscape_ref,
        transition_kind=transition_kind,
        transition_data=transition_data,
    )
