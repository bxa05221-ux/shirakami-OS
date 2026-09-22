"""Explicit EvidenceStore -> Landscape projection boundary."""

from collections.abc import Iterable

try:
    from .evidence import EvidenceRecord, is_transition_evidence
    from .evidence_store import EvidenceStore
    from .landscape import LandscapeState
except ImportError:
    from evidence import EvidenceRecord, is_transition_evidence
    from evidence_store import EvidenceStore
    from landscape import LandscapeState


def project_evidence(
    evidence: EvidenceRecord,
    landscape: LandscapeState,
) -> LandscapeState:
    """Apply only explicit transition evidence; observation remains evidence-only."""
    if not isinstance(evidence, EvidenceRecord):
        raise TypeError("project_evidence accepts EvidenceRecord only")
    if not isinstance(landscape, LandscapeState):
        raise TypeError("project_evidence accepts LandscapeState only")

    landscape.apply_evidence(evidence)
    return landscape


def project_store(
    store: EvidenceStore,
    landscape: LandscapeState,
) -> LandscapeState:
    """Project an EvidenceStore without mutating the store itself."""
    if not isinstance(store, EvidenceStore):
        raise TypeError("project_store accepts EvidenceStore only")
    if not isinstance(landscape, LandscapeState):
        raise TypeError("project_store accepts LandscapeState only")

    for evidence in store.all():
        project_evidence(evidence, landscape)
    return landscape


def is_projectable(evidence: EvidenceRecord) -> bool:
    """Expose the existing transition predicate without adding semantics."""
    if not isinstance(evidence, EvidenceRecord):
        raise TypeError("is_projectable accepts EvidenceRecord only")
    return is_transition_evidence(evidence)
