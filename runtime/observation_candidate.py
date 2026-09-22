"""Landscape Observation -> Protocol Candidate boundary for Runtime β0.1."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

try:
    from .landscape_observation import LandscapeObservation
except ImportError:
    from landscape_observation import LandscapeObservation


def _immutable_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(dict(value))


@dataclass(frozen=True)
class ProtocolCandidateArtifact:
    """Inspectable proposal derived from an Observation.

    This artifact is a candidate only. It carries no execution authority and
    cannot be promoted without the existing Human Gate.
    """

    candidate_identity: str
    origin_observation_identity: str
    origin: Mapping[str, Any]
    intent: Mapping[str, Any]
    assumptions: tuple[str, ...]
    inputs: tuple[str, ...]
    steps: tuple[str, ...]
    outputs: tuple[str, ...]
    constraints: tuple[str, ...]
    stop_conditions: tuple[str, ...]
    evidence_plan: Mapping[str, Any]
    approval: Mapping[str, Any]
    verification: Mapping[str, Any]
    status: str = "CANDIDATE"
    authority: bool = False
    executable: bool = False

    def __post_init__(self) -> None:
        if not self.candidate_identity:
            raise ValueError("candidate_identity is required")
        if not self.origin_observation_identity:
            raise ValueError("origin_observation_identity is required")
        if self.status != "CANDIDATE":
            raise ValueError("ProtocolCandidateArtifact must remain CANDIDATE")
        if self.authority:
            raise ValueError("ProtocolCandidateArtifact cannot carry authority")
        if self.executable:
            raise ValueError("ProtocolCandidateArtifact cannot be executable")

        object.__setattr__(self, "origin", _immutable_mapping(self.origin))
        object.__setattr__(self, "intent", _immutable_mapping(self.intent))
        object.__setattr__(self, "evidence_plan", _immutable_mapping(self.evidence_plan))
        object.__setattr__(self, "approval", _immutable_mapping(self.approval))
        object.__setattr__(self, "verification", _immutable_mapping(self.verification))

    @classmethod
    def from_observation(
        cls,
        observation: LandscapeObservation,
        *,
        candidate_identity: str,
        human_intent: Mapping[str, Any] | None = None,
    ) -> "ProtocolCandidateArtifact":
        """Create a minimal candidate without interpreting the observation."""
        if not isinstance(observation, LandscapeObservation):
            raise TypeError("observation must be a LandscapeObservation")

        return cls(
            candidate_identity=candidate_identity,
            origin_observation_identity=observation.observation_identity,
            origin={
                "observation_identity": observation.observation_identity,
                "observed_state": dict(observation.observed_state),
                "provenance": dict(observation.provenance),
                "uncertainty": observation.uncertainty,
                "source_landscape_context": dict(observation.source_landscape_context),
                "timestamp_or_run_context": dict(observation.timestamp_or_run_context),
            },
            intent=dict(human_intent or {}),
            assumptions=(
                "Observation is not domain truth.",
                "Candidate generation does not constitute authorization.",
            ),
            inputs=("Observation",),
            steps=(),
            outputs=(),
            constraints=(
                "Do not silently reinterpret observation as domain truth.",
                "Do not execute without Human Gate approval.",
            ),
            stop_conditions=("Human Gate approval is absent.",),
            evidence_plan={
                "execution_events": (),
                "expected_observations": (),
                "mismatch_handling": "preserve mismatch as Evidence",
            },
            approval={
                "required": True,
                "gate": "HUMAN_REVIEW",
            },
            verification={
                "separate_from_execution": True,
                "evaluator": "declared human or external verifier",
            },
        )
