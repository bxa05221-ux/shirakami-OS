"""Focused tests for the Landscape Observation boundary."""

import pytest

from runtime.landscape import LandscapeState
from runtime.landscape_observation import LandscapeObservation


def test_observation_captures_landscape_without_mutating_it() -> None:
    landscape = LandscapeState.from_snapshot({"status": "idle", "count": 2})
    before = landscape.snapshot()

    observation = LandscapeObservation.from_landscape(
        landscape,
        observation_identity="obs-001",
        provenance={"source": "runtime-test"},
        uncertainty="known",
        timestamp_or_run_context={"run_id": "run-001"},
    )

    assert landscape.snapshot() == before
    assert dict(observation.observed_state) == before
    assert observation.authority is False
    assert observation.executable is False


def test_observation_preserves_provenance_and_context() -> None:
    landscape = LandscapeState.from_snapshot({"status": "ready"})

    observation = LandscapeObservation.from_landscape(
        landscape,
        observation_identity="obs-002",
        provenance={"source": "landscape", "reason": "test"},
        uncertainty="partial",
        timestamp_or_run_context={"iteration": 1},
        source_landscape_context={"landscape_id": "L-1"},
    )

    assert dict(observation.provenance) == {
        "source": "landscape",
        "reason": "test",
    }
    assert observation.uncertainty == "partial"
    assert dict(observation.timestamp_or_run_context) == {"iteration": 1}
    assert dict(observation.source_landscape_context) == {"landscape_id": "L-1"}


def test_observation_state_is_immutable() -> None:
    landscape = LandscapeState.from_snapshot({"status": "idle"})

    observation = LandscapeObservation.from_landscape(
        landscape,
        observation_identity="obs-003",
        provenance={},
        uncertainty="known",
        timestamp_or_run_context={},
    )

    with pytest.raises(TypeError):
        observation.observed_state["status"] = "changed"  # type: ignore[index]


def test_observation_rejects_authority_or_executable_flags() -> None:
    with pytest.raises(ValueError, match="authority"):
        LandscapeObservation(
            observation_identity="obs-004",
            source_landscape_context={},
            observed_state={},
            provenance={},
            uncertainty="known",
            timestamp_or_run_context={},
            authority=True,
        )

    with pytest.raises(ValueError, match="executable"):
        LandscapeObservation(
            observation_identity="obs-005",
            source_landscape_context={},
            observed_state={},
            provenance={},
            uncertainty="known",
            timestamp_or_run_context={},
            executable=True,
        )


def test_observation_requires_identity() -> None:
    with pytest.raises(ValueError, match="observation_identity"):
        LandscapeObservation(
            observation_identity="",
            source_landscape_context={},
            observed_state={},
            provenance={},
            uncertainty="known",
            timestamp_or_run_context={},
        )
