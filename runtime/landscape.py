"""Minimal replaceable Landscape State boundary for Runtime β0.1."""

from dataclasses import dataclass, field
from typing import Any, Mapping

try:
    from .evidence import EvidenceRecord, is_transition_evidence
except ImportError:  # legacy top-level runtime test imports
    from evidence import EvidenceRecord, is_transition_evidence


@dataclass
class LandscapeState:
    """Small in-memory representation of current observable Landscape state."""

    _state: dict[str, Any]
    evidence: list[EvidenceRecord] = field(default_factory=list)

    @classmethod
    def empty(cls) -> "LandscapeState":
        return cls(_state={})

    def snapshot(self) -> Mapping[str, Any]:
        return dict(self._state)

    def apply_evidence(self, evidence: EvidenceRecord) -> None:
        """Apply only evidence explicitly representing a Landscape transition."""
        if not is_transition_evidence(evidence):
            return

        self.evidence.append(evidence)
        self._state.update(dict(evidence.transition_data))
