"""Observation -> Protocol Candidate semantic eligibility boundary.

This module implements only the Research-defined sufficiency checks. It does
not rank, select, approve, promote, activate, or interpret domain semantics.
"""

from dataclasses import dataclass
from typing import Any

try:
    from .landscape_observation import LandscapeObservation
except ImportError:
    from landscape_observation import LandscapeObservation


@dataclass(frozen=True)
class CandidateEligibilityResult:
    """Immutable result of Observation semantic sufficiency assessment."""

    eligible: bool
    reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.eligible and self.reasons:
            raise ValueError("eligible result cannot contain failure reasons")


_REQUIRED_FIELDS = (
    "observation_identity",
    "source_landscape_context",
    "observed_state",
    "provenance",
    "uncertainty",
    "timestamp_or_run_context",
)


def assess_candidate_eligibility(
    observation: LandscapeObservation,
) -> CandidateEligibilityResult:
    """Assess whether an Observation is semantically sufficient for a Candidate.

    The assessment is deliberately domain-agnostic. It checks traceability,
    context, temporal binding, uncertainty, and preservation of observed state.
    It never infers domain truth or candidate value.
    """
    if not isinstance(observation, LandscapeObservation):
        raise TypeError("observation must be a LandscapeObservation")

    reasons: list[str] = []

    if not observation.observation_identity:
        reasons.append("missing_observation_identity")
    if not observation.source_landscape_context:
        reasons.append("missing_source_landscape_context")
    if observation.observed_state is None:
        reasons.append("missing_observed_state")
    if not observation.provenance:
        reasons.append("missing_provenance")
    if not observation.uncertainty:
        reasons.append("missing_uncertainty")
    if not observation.timestamp_or_run_context:
        reasons.append("missing_timestamp_or_run_context")

    if observation.authority:
        reasons.append("observation_has_authority")
    if observation.executable:
        reasons.append("observation_is_executable")

    return CandidateEligibilityResult(
        eligible=not reasons,
        reasons=tuple(reasons),
    )


def require_candidate_eligibility(
    observation: LandscapeObservation,
) -> None:
    """Fail closed when an Observation is not semantically sufficient."""
    result = assess_candidate_eligibility(observation)
    if not result.eligible:
        raise ValueError(
            "Observation is not eligible for Candidate generation: "
            + ", ".join(result.reasons)
        )
