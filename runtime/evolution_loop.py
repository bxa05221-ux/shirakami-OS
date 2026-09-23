"""Minimal end-to-end Evolution Loop composition for Runtime β0.1."""

from __future__ import annotations

from typing import Any, Mapping

from .backend import Backend
from .evidence_return_backend import evidence_from_backend_response


def execute_and_observe(
    backend: Backend,
    handoff: Mapping[str, Any],
    *,
    protocol_id: str = "evolution-loop.v0.1",
):
    """Execute a previously authorized handoff and record only the observed result."""
    response = backend.execute(handoff)
    return evidence_from_backend_response(response, protocol_id=protocol_id)
