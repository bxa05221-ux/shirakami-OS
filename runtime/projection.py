"""Explicit Evidence -> Landscape Projection boundary for Runtime β0.1.

Projection is kept separate from Evidence capture so Evidence remains an
immutable execution record while LandscapeState remains the current view.
No new protocol semantics are introduced here.
"""

from typing import Any, Mapping

from evidence import EvidenceRecord
from landscape import LandscapeState


def project_evidence(
    evidence: EvidenceRecord,
    state: LandscapeState | None = None,
) -> Mapping[str, Any]:
    """Project immutable Evidence into a replaceable Landscape state view."""

    target = state if state is not None else LandscapeState.empty()
    target.apply_evidence(evidence)
    return target.snapshot()
