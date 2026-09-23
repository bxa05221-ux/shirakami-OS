"""Minimal HTTP-facing Evolution Loop v0.1 adapter.

This module intentionally keeps the API boundary thin: it accepts an already
authorized SemanticHandoff-shaped mapping, delegates execution to the
Runtime primitive, and returns the resulting EvidenceRecord as JSON-ready data.
No decision is inferred here and HumanGate authorization is not bypassed.
"""

from __future__ import annotations

from typing import Any, Mapping

from runtime.backend import Backend
from runtime.evolution_loop import execute_and_observe


def execute_evolution_v0_1(
    backend: Backend,
    handoff: Mapping[str, Any],
) -> dict[str, Any]:
    """Execute an authorized handoff and return observed Evidence as JSON data."""
    evidence = execute_and_observe(backend, handoff)
    return {
        "evidence_id": evidence.evidence_id,
        "protocol_id": evidence.protocol_id,
        "status": evidence.status,
        "transition_kind": evidence.transition_kind,
        "transition_data": dict(evidence.transition_data),
        "signals": list(evidence.signals),
        "confidence": evidence.confidence,
    }
