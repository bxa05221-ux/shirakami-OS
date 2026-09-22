"""Tests for the Candidate Eligibility -> Candidate Generation boundary."""

import pytest

from runtime.candidate_generation import generate_protocol_candidate
from runtime.landscape_observation import LandscapeObservation


def make_observation(**overrides):
    values = {
        "observation_identity": "obs-001",
        "source_landscape_context": {"source": "test"},
        "observed_state": {"state": "observed"},
        "provenance": {"run_id": "run-001"},
        "uncertainty": "observed-with-uncertainty",
        "timestamp_or_run_context": {"timestamp": "2026-09-22T00:00:00Z"},
    }
    values.update(overrides)
    return LandscapeObservation(**values)


def test_eligible_observation_generates_candidate():
    observation = make_observation()

    candidate = generate_protocol_candidate(
        observation,
        candidate_identity="candidate-001",
    )

    assert candidate.status == "CANDIDATE"
    assert candidate.authority is False
    assert candidate.executable is False
    assert candidate.origin_observation_identity == observation.observation_identity


def test_provenance_and_uncertainty_are_preserved():
    observation = make_observation(
        provenance={"run_id": "run-777", "source": "observation"},
        uncertainty="high-uncertainty",
    )

    candidate = generate_protocol_candidate(
        observation,
        candidate_identity="candidate-002",
    )

    assert candidate.origin["provenance"] == observation.provenance
    assert candidate.origin["uncertainty"] == observation.uncertainty
    assert candidate.origin["timestamp_or_run_context"] == observation.timestamp_or_run_context


def test_missing_context_fails_closed_before_generation():
    observation = make_observation(provenance={})

    with pytest.raises(ValueError, match="missing_provenance"):
        generate_protocol_candidate(
            observation,
            candidate_identity="candidate-003",
        )


def test_missing_semantics_are_not_invented():
    candidate = generate_protocol_candidate(
        make_observation(),
        candidate_identity="candidate-004",
    )

    assert candidate.steps == ()
    assert candidate.outputs == ()


def test_generation_does_not_rank_or_select():
    candidate = generate_protocol_candidate(
        make_observation(),
        candidate_identity="candidate-005",
    )

    assert not hasattr(candidate, "score")
    assert not hasattr(candidate, "priority")


def test_human_intent_is_explicit_input_not_generated_domain_truth():
    candidate = generate_protocol_candidate(
        make_observation(),
        candidate_identity="candidate-006",
        human_intent={"purpose": "inspect"},
    )

    assert candidate.intent == {"purpose": "inspect"}
    assert candidate.authority is False
    assert candidate.executable is False


def test_generation_does_not_create_approval_or_activation():
    candidate = generate_protocol_candidate(
        make_observation(),
        candidate_identity="candidate-007",
    )

    assert candidate.approval["required"] is True
    assert candidate.approval["gate"] == "HUMAN_REVIEW"
    assert not hasattr(candidate, "activation")
