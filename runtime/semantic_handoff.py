from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class SemanticHandoff:
    """Immutable cross-boundary context envelope; never an authority artifact."""

    observation_id: str
    landscape: Mapping[str, Any] = field(default_factory=dict)
    protocol_id: str = ""
    runtime_state: str = ""
    evidence_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def as_mapping(self) -> Mapping[str, Any]:
        return {
            "observation_id": self.observation_id,
            "landscape": dict(self.landscape),
            "protocol_id": self.protocol_id,
            "runtime_state": self.runtime_state,
            "evidence_ids": tuple(self.evidence_ids),
            "metadata": dict(self.metadata),
        }
