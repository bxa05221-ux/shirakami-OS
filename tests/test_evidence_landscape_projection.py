"""Tests for the explicit EvidenceStore -> Landscape projection boundary."""

from runtime.evidence import EvidenceRecord
from runtime.evidence_store import EvidenceStore
from runtime.evidence_landscape_projection import is_projectable, project_store
from runtime.landscape import LandscapeState


def runner_observation() -> EvidenceRecord:
    return EvidenceRecord(
        protocol_id="protocol-1",
        status="observed",
        transition_kind="runner:iteration_completed",
        transition_data={
            "run_identity": "run-1",
            "iteration": 1,
            "runner_state": "VERIFYING",
        },
        signals=("RUNNER_OBSERVED",),
    )


def explicit_transition() -> EvidenceRecord:
    return EvidenceRecord(
        protocol_id="protocol-1",
        status="observed",
        transition_kind="R0100:transition",
        transition_data={"changed": True, "phase": "completed"},
        signals=("TRANSITION",),
    )


def test_runner_observation_is_not_projectable():
    evidence = runner_observation()
    assert is_projectable(evidence) is False

    store = EvidenceStore().append(evidence)
    landscape = LandscapeState.empty()
    project_store(store, landscape)

    assert landscape.snapshot() == {}
    assert landscape.evidence == []


def test_explicit_transition_is_projected():
    evidence = explicit_transition()
    assert is_projectable(evidence) is True

    store = EvidenceStore().append(evidence)
    landscape = LandscapeState.empty()
    project_store(store, landscape)

    assert landscape.snapshot()["phase"] == "completed"
    assert landscape.evidence == [evidence]


def test_projection_does_not_mutate_evidence_store():
    observation = runner_observation()
    transition = explicit_transition()
    store = EvidenceStore().extend((observation, transition))
    before = store.all()

    landscape = LandscapeState.empty()
    project_store(store, landscape)

    assert store.all() == before
    assert len(store.all()) == 2


def test_projection_does_not_create_authority_or_change_records():
    evidence = runner_observation()
    store = EvidenceStore().append(evidence)
    landscape = LandscapeState.empty()

    project_store(store, landscape)

    assert store.all() == (evidence,)
    assert landscape.evidence == []
