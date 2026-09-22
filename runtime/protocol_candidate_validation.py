"""Explicit ProtocolCandidateArtifact -> structural validation boundary."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

try:
    from .observation_candidate import ProtocolCandidateArtifact
except ImportError:
    from observation_candidate import ProtocolCandidateArtifact


@dataclass(frozen=True)
class StructuralValidationRepresentation:
    """Immutable, non-authoritative representation for structural inspection."""

    candidate_identity: str
    origin_observation_identity: str
    candidate: Mapping[str, Any]
    authority: bool = False
    executable: bool = False

    def __post_init__(self) -> None:
        if not self.candidate_identity:
            raise ValueError("candidate_identity is required")
        if not self.origin_observation_identity:
            raise ValueError("origin_observation_identity is required")
        if self.authority:
            raise ValueError("validation representation cannot carry authority")
        if self.executable:
            raise ValueError("validation representation cannot be executable")
        object.__setattr__(
            self, "candidate", MappingProxyType(dict(self.candidate))
        )


def to_structural_validation_representation(
    artifact: ProtocolCandidateArtifact,
) -> StructuralValidationRepresentation:
    """Map only explicit Artifact fields; add no semantic or execution authority."""
    if not isinstance(artifact, ProtocolCandidateArtifact):
        raise TypeError("artifact must be a ProtocolCandidateArtifact")

    candidate = {
        "candidate_identity": artifact.candidate_identity,
        "origin_observation_identity": artifact.origin_observation_identity,
        "origin": dict(artifact.origin),
        "intent": dict(artifact.intent),
        "assumptions": tuple(artifact.assumptions),
        "inputs": tuple(artifact.inputs),
        "steps": tuple(artifact.steps),
        "outputs": tuple(artifact.outputs),
        "constraints": tuple(artifact.constraints),
        "stop_conditions": tuple(artifact.stop_conditions),
        "evidence_plan": dict(artifact.evidence_plan),
        "approval": dict(artifact.approval),
        "verification": dict(artifact.verification),
        "status": artifact.status,
        "authority": artifact.authority,
        "executable": artifact.executable,
    }
    return StructuralValidationRepresentation(
        candidate_identity=artifact.candidate_identity,
        origin_observation_identity=artifact.origin_observation_identity,
        candidate=candidate,
    )
