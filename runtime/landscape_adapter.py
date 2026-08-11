"""Replaceable Landscape Adapter boundary for Runtime β0.1."""

from typing import Any, Mapping, Protocol

from evidence import EvidenceRecord, is_transition_evidence


class LandscapeAdapter(Protocol):
    def read_state(self) -> Mapping[str, Any]: ...

    def apply_transition(self, evidence: EvidenceRecord) -> None: ...


class InMemoryLandscapeAdapter:
    """Minimal external Landscape implementation used for boundary testing."""

    def __init__(self, initial_state: Mapping[str, Any] | None = None) -> None:
        self._state = dict(initial_state or {})

    def read_state(self) -> Mapping[str, Any]:
        return dict(self._state)

    def apply_transition(self, evidence: EvidenceRecord) -> None:
        if not is_transition_evidence(evidence):
            return
        self._state.update(dict(evidence.transition_data))
