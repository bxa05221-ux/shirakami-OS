"""Tests for the Observation -> Candidate semantic sufficiency boundary."""

import pytest

from runtime.landscape_observation import LandscapeObservation
from runtime.observation_candidate_eligibility import (
    assess_candidate_eligibility,
    require_candidate_eligibility,
)


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


def test_complete_observation_is_eligible():
    result = assess_candidate_eligibility(make_observation())

    assert result.eligible is True
    assert result.reasons == ()


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("source_landscape_context", {}, "missing_source_landscape_context"),
        ("provenance", {}, "missing_provenance"),
        ("uncertainty", "", "missing_uncertainty"),
        ("timestamp_or_run_context", {}, "missing_timestamp_or_run_context"),
    ],
)
def test_missing_required_context_fails_closed(field, value, reason):
    result = assess_candidate_eligibility(make_observation(**{field: value}))

    assert result.eligible is False
    assert reason in result.reasons


def test_missing_observation_identity_fails_closed_at_observation_boundary():
    with pytest.raises(ValueError, match="observation_identity is required"):
        make_observation(observation_identity="")


def test_empty_observed_state_is_still_an_observed_state():
    result = assess_candidate_eligibility(
        make_observation(observed_state={})
    )

    assert result.eligible is True


def test_uncertainty_does_not_by_itself_reject_observation():
    result = assess_candidate_eligibility(
        make_observation(uncertainty="high-uncertainty")
    )

    assert result.eligible is True


def test_eligibility_does_not_rank_or_select_candidates():
    result = assess_candidate_eligibility(make_observation())

    assert result.eligible is True
    assert not hasattr(result, "score")
    assert not hasattr(result, "priority")


def test_require_fails_closed_for_missing_context():
    with pytest.raises(ValueError, match="missing_provenance"):
        require_candidate_eligibility(
            make_observation(provenance={})
        )


def test_observation_remains_non_authoritative_and_non_executable():
    observation = make_observation()

    assert observation.authority is False
    assert observation.executable is False
