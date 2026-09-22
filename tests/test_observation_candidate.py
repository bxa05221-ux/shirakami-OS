"""Focused tests for the Observation -> Protocol Candidate boundary."""

import pytest

from runtime.landscape import LandscapeState
from runtime.landscape_observation import LandscapeObservation
from runtime.observation_candidate import ProtocolCandidateArtifact


def _observation() -> LandscapeObservation:
    return LandscapeObservation.from_landscape(
        LandscapeState.from_snapshot({"status": "observed"}),
        observation_identity="obs-100",
        provenance={"source": "test"},
        uncertainty="partial",
        timestamp_or_run_context={"run_id": "run-100"},
        source_landscape_context={"landscape_id": "L-100"},
    )


def test_candidate_preserves_observation_origin_without_mutating_it() -> None:
    observation = _observation()
    before = dict(observation.observed_state)

    candidate = ProtocolCandidateArtifact.from_observation(
        observation,
        candidate_identity="candidate-100",
        human_intent={"objective": "inspect"},
    )

    assert dict(observation.observed_state) == before
    assert candidate.origin_observation_identity == "obs-100"
    assert candidate.origin["observation_identity"] == "obs-100"
    assert candidate.origin["uncertainty"] == "partial"
    assert dict(candidate.intent) == {"objective": "inspect"}


def test_candidate_is_not_authorized_or_executable() -> None:
    candidate = ProtocolCandidateArtifact.from_observation(
        _observation(),
        candidate_identity="candidate-101",
    )

    assert candidate.status == "CANDIDATE"
    assert candidate.authority is False
    assert candidate.executable is False
    assert candidate.approval["required"] is True
    assert candidate.approval["gate"] == "HUMAN_REVIEW"


def test_candidate_does_not_invent_protocol_steps_or_outputs() -> None:
    candidate = ProtocolCandidateArtifact.from_observation(
        _observation(),
        candidate_identity="candidate-102",
    )

    assert candidate.steps == ()
    assert candidate.outputs == ()
    assert candidate.evidence_plan["execution_events"] == ()


def test_candidate_rejects_non_observation_input() -> None:
    with pytest.raises(TypeError, match="LandscapeObservation"):
        ProtocolCandidateArtifact.from_observation(
            object(),
            candidate_identity="candidate-103",
        )


def test_candidate_rejects_promotion_flags() -> None:
    with pytest.raises(ValueError, match="authority"):
        ProtocolCandidateArtifact(
            candidate_identity="candidate-104",
            origin_observation_identity="obs-104",
            origin={},
            intent={},
            assumptions=(),
            inputs=(),
            steps=(),
            outputs=(),
            constraints=(),
            stop_conditions=(),
            evidence_plan={},
            approval={"required": True, "gate": "HUMAN_REVIEW"},
            verification={"separate_from_execution": True},
            authority=True,
        )
