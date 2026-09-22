from dataclasses import FrozenInstanceError

import pytest

from runtime.observation_candidate import ProtocolCandidateArtifact
from runtime.protocol_candidate_validation import (
    StructuralValidationRepresentation,
    to_structural_validation_representation,
)
from runtime.structural_validation_representation_validator import (
    validate_structural_validation_representation,
)


def make_representation() -> StructuralValidationRepresentation:
    artifact = ProtocolCandidateArtifact(
        candidate_identity="candidate-001",
        origin_observation_identity="observation-001",
        origin={
            "observation_identity": "observation-001",
            "observed_state": {"mode": "observed"},
            "provenance": {"source": "test"},
            "uncertainty": "test-uncertainty",
        },
        intent={"objective": "inspect"},
        assumptions=("Observation is not domain truth.",),
        inputs=("Observation",),
        steps=(),
        outputs=(),
        constraints=("No execution without Human Gate.",),
        stop_conditions=("Human Gate approval is absent.",),
        evidence_plan={
            "execution_events": (),
            "expected_observations": (),
            "mismatch_handling": "preserve mismatch as Evidence",
        },
        approval={"required": True, "gate": "HUMAN_REVIEW"},
        verification={
            "separate_from_execution": True,
            "evaluator": "declared verifier",
        },
    )
    return to_structural_validation_representation(artifact)


def test_valid_representation_passes_structure_only():
    representation = make_representation()

    result = validate_structural_validation_representation(representation)

    assert result["valid"] is True
    assert result["errors"] == ()
    assert result["candidate_identity"] == "candidate-001"
    assert result["origin_observation_identity"] == "observation-001"
    assert result["authority"] is False
    assert result["executable"] is False


def test_missing_explicit_field_fails_closed():
    representation = make_representation()
    candidate = dict(representation.candidate)
    candidate.pop("evidence_plan")

    malformed = StructuralValidationRepresentation(
        candidate_identity=representation.candidate_identity,
        origin_observation_identity=representation.origin_observation_identity,
        candidate=candidate,
    )

    result = validate_structural_validation_representation(malformed)

    assert result["valid"] is False
    assert any("evidence_plan" in error for error in result["errors"])


def test_invalid_status_fails_closed():
    representation = make_representation()
    candidate = dict(representation.candidate)
    candidate["status"] = "READY"

    malformed = StructuralValidationRepresentation(
        candidate_identity=representation.candidate_identity,
        origin_observation_identity=representation.origin_observation_identity,
        candidate=candidate,
    )

    result = validate_structural_validation_representation(malformed)

    assert result["valid"] is False
    assert "candidate.status must be CANDIDATE" in result["errors"]


def test_authority_or_execution_cannot_pass():
    representation = make_representation()

    with pytest.raises(ValueError):
        StructuralValidationRepresentation(
            candidate_identity=representation.candidate_identity,
            origin_observation_identity=representation.origin_observation_identity,
            candidate=dict(representation.candidate),
            authority=True,
        )

    with pytest.raises(ValueError):
        StructuralValidationRepresentation(
            candidate_identity=representation.candidate_identity,
            origin_observation_identity=representation.origin_observation_identity,
            candidate=dict(representation.candidate),
            executable=True,
        )


def test_provenance_mismatch_fails_closed():
    representation = make_representation()
    candidate = dict(representation.candidate)
    candidate["origin"] = {
        "observation_identity": "different-observation",
        "observed_state": {},
    }

    malformed = StructuralValidationRepresentation(
        candidate_identity=representation.candidate_identity,
        origin_observation_identity=representation.origin_observation_identity,
        candidate=candidate,
    )

    result = validate_structural_validation_representation(malformed)

    assert result["valid"] is False
    assert "origin.observation_identity must preserve provenance" in result["errors"]


def test_empty_steps_and_outputs_are_not_treated_as_missing_semantics():
    representation = make_representation()

    assert representation.candidate["steps"] == ()
    assert representation.candidate["outputs"] == ()

    result = validate_structural_validation_representation(representation)

    assert result["valid"] is True


def test_validation_does_not_mutate_representation():
    representation = make_representation()
    before = dict(representation.candidate)

    validate_structural_validation_representation(representation)

    assert dict(representation.candidate) == before
    with pytest.raises(TypeError):
        representation.candidate["status"] = "READY"


def test_missing_provenance_or_uncertainty_fails_closed():
    representation = make_representation()

    for field in ("provenance", "uncertainty"):
        candidate = dict(representation.candidate)
        origin = dict(candidate["origin"])
        origin.pop(field)
        candidate["origin"] = origin

        malformed = StructuralValidationRepresentation(
            candidate_identity=representation.candidate_identity,
            origin_observation_identity=representation.origin_observation_identity,
            candidate=candidate,
        )

        result = validate_structural_validation_representation(malformed)

        assert result["valid"] is False
        assert any(field in error for error in result["errors"])