import pytest

from runtime.activation import activate_approved_protocol
from runtime.activation_pump import release_activation
from runtime.approval_envelope_activation import to_activation_input
from runtime.background_runner import RunnerState, run_released_activation
from runtime.evidence import EvidenceRecord
from runtime.evidence_landscape_projection import is_projectable, project_store
from runtime.evidence_store import EvidenceStore
from runtime.landscape import LandscapeState
from runtime.landscape_observation import LandscapeObservation
from runtime.observation_candidate import ProtocolCandidateArtifact
from runtime.protocol_candidate_validation import (
    to_structural_validation_representation,
)
from runtime.runner_evidence_store import append_runner_evidence
from runtime.structural_validation_human_gate import process_validated_candidate
from runtime.structural_validation_representation_validator import (
    validate_structural_validation_representation,
)


def build_approved_release():
    landscape = LandscapeState.empty()
    initial_snapshot = landscape.snapshot()

    observation = LandscapeObservation.from_landscape(
        landscape,
        observation_identity="observation-e2e-001",
        provenance={"source": "runtime-loop-test"},
        uncertainty="test",
        timestamp_or_run_context={"run": "e2e-001"},
    )
    assert landscape.snapshot() == initial_snapshot

    artifact = ProtocolCandidateArtifact.from_observation(
        observation,
        candidate_identity="candidate-e2e-001",
        human_intent={"objective": "verify runtime loop"},
    )
    representation = to_structural_validation_representation(artifact)
    validation = validate_structural_validation_representation(representation)

    assert validation["valid"] is True
    assert validation["authority"] is False
    assert validation["executable"] is False

    validated = {
        **validation,
        "protocol_identity": "protocol-e2e-001",
        "provenance": ("observation-e2e-001",),
        "evidence_ids": ("evidence-plan-e2e-001",),
    }

    decision = process_validated_candidate(
        validation_result=validated,
        reviewer_identity="human-e2e-001",
        decision="approve",
    )
    envelope = decision.approval_envelope
    assert envelope is not None
    assert envelope.execution_authorized is True
    assert envelope.approval_scope == "execution"

    activation_input = to_activation_input(envelope)
    activation = activate_approved_protocol(
        approval=activation_input,
        activation_id="activation-e2e-001",
    )
    assert activation.released is False

    released = release_activation(
        activation=activation,
        release_id="release-e2e-001",
    )
    return landscape, observation, released


def test_runtime_loop_end_to_end_preserves_boundaries():
    landscape, observation, released = build_approved_release()

    result = run_released_activation(
        activation=released,
        iteration_budget=1,
        run_id="runner-e2e-001",
        execute=lambda _activation, _iteration: True,
        verify=lambda _activation, _iteration: True,
    )

    assert result.state is RunnerState.COMPLETED
    assert result.protocol_identity == "protocol-e2e-001"
    assert result.activation_identity == "activation-e2e-001"
    assert result.approval_identity == "human-e2e-001"
    assert result.evidence

    store = append_runner_evidence(
        EvidenceStore(),
        result.evidence,
        protocol_id=result.protocol_identity,
    )
    assert len(store.all()) == len(result.evidence)
    assert all(not is_projectable(record) for record in store.all())
    assert landscape.snapshot() == {}

    next_observation = LandscapeObservation.from_landscape(
        landscape,
        observation_identity="observation-e2e-002",
        provenance={"source": "runner-e2e-001"},
        uncertainty="test",
        timestamp_or_run_context={"run": "e2e-001"},
    )
    assert next_observation.observed_state == {}
    assert next_observation.authority is False
    assert next_observation.executable is False


def test_runner_verification_mismatch_stops_and_emits_evidence():
    _landscape, _observation, released = build_approved_release()

    result = run_released_activation(
        activation=released,
        iteration_budget=1,
        run_id="runner-e2e-mismatch-001",
        execute=lambda _activation, _iteration: True,
        verify=lambda _activation, _iteration: False,
    )

    assert result.state is RunnerState.STOPPED
    assert any(
        evidence.event == "runner_stopped"
        for evidence in result.evidence
    )


def test_only_explicit_transition_evidence_changes_landscape():
    landscape = LandscapeState.empty()

    observed = EvidenceRecord(
        protocol_id="protocol-e2e-001",
        status="observed",
        transition_kind="runner:runner_stopped",
        transition_data={"changed": False, "runner_state": "STOPPED"},
        signals=("runner:runner_stopped",),
    )
    transition = EvidenceRecord(
        protocol_id="protocol-e2e-001",
        status="observed",
        transition_kind="explicit:landscape_transition",
        transition_data={"changed": True, "phase": "verified"},
        signals=("transition:verified",),
    )

    store = EvidenceStore().extend((observed, transition))
    project_store(store, landscape)

    assert landscape.snapshot() == {
        "changed": True,
        "phase": "verified",
    }
    assert len(store.all()) == 2


def test_observation_is_not_executable_or_authoritative():
    landscape = LandscapeState.empty()
    observation = LandscapeObservation.from_landscape(
        landscape,
        observation_identity="observation-boundary-001",
        provenance={},
        uncertainty="unknown",
        timestamp_or_run_context={},
    )

    assert observation.authority is False
    assert observation.executable is False


def test_approved_pipeline_e2e_returns_to_observation_without_landscape_mutation():
    from runtime.pipeline_runner import run_approved_pipeline_on_runner

    landscape, _observation, released = build_approved_release()

    pipeline_result = run_approved_pipeline_on_runner(
        pipeline_identity="pipeline-e2e-001",
        activations=(released,),
        iteration_budget=1,
        execute=lambda _activation, _iteration: True,
        verify=lambda _activation, _iteration: True,
    )

    assert pipeline_result.stopped is False
    assert pipeline_result.runner_results[0].state is RunnerState.COMPLETED
    assert pipeline_result.items
    assert all(item.pipeline_identity == "pipeline-e2e-001" for item in pipeline_result.items)
    assert all(item.execution_order == 1 for item in pipeline_result.items)
    assert all(item.run_identity == "pipeline-e2e-001:run:1" for item in pipeline_result.items)

    assert landscape.snapshot() == {}

    next_observation = LandscapeObservation.from_landscape(
        landscape,
        observation_identity="observation-pipeline-002",
        provenance={
            "source": "pipeline-e2e-001",
            "runner_run": "pipeline-e2e-001:run:1",
        },
        uncertainty="observed",
        timestamp_or_run_context={"pipeline": "pipeline-e2e-001"},
    )

    assert next_observation.observed_state == {}
    assert next_observation.authority is False
    assert next_observation.executable is False
