from runtime.landscape_observation import LandscapeObservation
from runtime.observation_candidate import ProtocolCandidateArtifact
from runtime.protocol_candidate_validation import (
    StructuralValidationRepresentation,
    to_structural_validation_representation,
)


def make_artifact():
    observation = LandscapeObservation.from_landscape(
        __import__("runtime.landscape", fromlist=["LandscapeState"]).LandscapeState.empty(),
        observation_identity="obs-001",
        provenance={"source": "test"},
        uncertainty="unknown",
        timestamp_or_run_context={"run": "test"},
    )
    return ProtocolCandidateArtifact.from_observation(
        observation,
        candidate_identity="candidate-001",
        human_intent={"objective": "inspect"},
    )


def test_adapter_preserves_identity_and_explicit_fields():
    artifact = make_artifact()
    result = to_structural_validation_representation(artifact)

    assert isinstance(result, StructuralValidationRepresentation)
    assert result.candidate_identity == "candidate-001"
    assert result.origin_observation_identity == "obs-001"
    assert result.candidate["origin"]["observation_identity"] == "obs-001"
    assert result.candidate["intent"]["objective"] == "inspect"
    assert result.candidate["status"] == "CANDIDATE"


def test_adapter_does_not_add_authority_or_execution():
    result = to_structural_validation_representation(make_artifact())

    assert result.authority is False
    assert result.executable is False
    assert result.candidate["authority"] is False
    assert result.candidate["executable"] is False


def test_adapter_preserves_empty_steps_and_outputs():
    result = to_structural_validation_representation(make_artifact())

    assert result.candidate["steps"] == ()
    assert result.candidate["outputs"] == ()


def test_adapter_does_not_mutate_artifact():
    artifact = make_artifact()
    before = artifact.origin
    to_structural_validation_representation(artifact)

    assert artifact.origin == before


def test_adapter_rejects_non_artifact():
    try:
        to_structural_validation_representation({})
    except TypeError as exc:
        assert "ProtocolCandidateArtifact" in str(exc)
    else:
        raise AssertionError("expected TypeError")


def test_representation_is_immutable_mapping():
    result = to_structural_validation_representation(make_artifact())

    try:
        result.candidate["status"] = "APPROVED"
    except TypeError:
        pass
    else:
        raise AssertionError("candidate mapping must be immutable")
