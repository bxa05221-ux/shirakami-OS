"""Runtime adapter for the Research-defined Candidate Generation boundary."""

from typing import Any, Mapping

try:
    from .landscape_observation import LandscapeObservation
    from .observation_candidate import ProtocolCandidateArtifact
    from .observation_candidate_eligibility import require_candidate_eligibility
except ImportError:
    from landscape_observation import LandscapeObservation
    from observation_candidate import ProtocolCandidateArtifact
    from observation_candidate_eligibility import require_candidate_eligibility


def generate_protocol_candidate(
    observation: LandscapeObservation,
    *,
    candidate_identity: str,
    human_intent: Mapping[str, Any] | None = None,
) -> ProtocolCandidateArtifact:
    """Generate a non-authoritative Candidate from an eligible Observation.

    Eligibility is checked before generation. This adapter does not rank,
    select, approve, promote, activate, mutate Landscape state, or invent
    domain semantics.
    """
    require_candidate_eligibility(observation)

    return ProtocolCandidateArtifact.from_observation(
        observation,
        candidate_identity=candidate_identity,
        human_intent=human_intent,
    )
