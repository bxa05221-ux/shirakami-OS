"""Minimal Evidence -> Projection -> Landscape boundary for β0.1.

Projection is intentionally kept separate from Evidence and LandscapeState.
Evidence remains immutable observation; Projection is the derived operation that
maps an eligible EvidenceRecord into a state update without mutating the
Evidence itself.
"""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from evidence import EvidenceRecord, is_transition_evidence


@dataclass(frozen=True)
class Projection:
    """Immutable projection of one EvidenceRecord into Landscape state."""

    evidence_id: str
    changes: Mapping[str, Any]


class ProjectionError(ValueError):
    """Raised when an EvidenceRecord cannot be projected."""


def project_evidence(evidence: EvidenceRecord) -> Projection:
    """Create a pure Projection from transition Evidence."""

    if not is_transition_evidence(evidence):
        raise ProjectionError("Evidence does not represent a Landscape transition")

    # β0.1 has no canonical Evidence ID yet. Preserve source identity using
    # the immutable protocol/status/transition tuple as a deterministic key.
    evidence_id = ":".join(
        (evidence.protocol_id, evidence.status, evidence.transition_kind)
    )
    return Projection(
        evidence_id=evidence_id,
        changes=MappingProxyType(dict(evidence.transition_data)),
    )
