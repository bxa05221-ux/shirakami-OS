"""Minimal gate for declared Protocol applicability conditions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .protocol_input import ProtocolInput


@dataclass(frozen=True)
class ApplicabilityResult:
    protocol_id: str
    applicable: bool
    unresolved_questions: tuple[str, ...] = ()
    failed_conditions: tuple[str, ...] = ()


def evaluate_applicability(
    protocol_input: ProtocolInput,
    protocol_id: str,
    conditions: Mapping[str, object],
    *,
    available: Mapping[str, object] | None = None,
) -> ApplicabilityResult:
    """Evaluate only explicitly declared, directly available conditions.

    This gate does not infer meaning. A missing condition is unresolved rather
    than fabricated, and a mismatched declared value makes the protocol
    inapplicable.
    """
    available = {} if available is None else available
    unresolved: list[str] = []
    failed: list[str] = []

    for name, expected in conditions.items():
        if name not in available:
            unresolved.append(f"condition unavailable: {name}")
            continue
        if available[name] != expected:
            failed.append(name)

    return ApplicabilityResult(
        protocol_id=protocol_id,
        applicable=not unresolved and not failed,
        unresolved_questions=tuple(unresolved),
        failed_conditions=tuple(failed),
    )
