"""Anmon inquiry data uses the generic non-authoritative candidate boundary."""

from runtime.landscape import LandscapeState
from runtime.landscape_observation import LandscapeObservation
from runtime.observation_candidate import ProtocolCandidateArtifact
from runtime.protocol_candidate_validation import to_structural_validation_representation


def test_inquiry_data_survives_handoff_without_granting_authority() -> None:
    observation = LandscapeObservation.from_landscape(
        LandscapeState.from_snapshot({"topic": "uncertain"}),
        observation_identity="anmon-observation-1",
        provenance={"source": "anmon-protocol"},
        uncertainty="unresolved",
        timestamp_or_run_context={"run_id": "anmon-run-1"},
        source_landscape_context={"landscape_id": "anmon-landscape-1"},
    )

    candidate = ProtocolCandidateArtifact.from_observation(
        observation,
        candidate_identity="anmon-candidate-1",
        human_intent={
            "questions": ["What evidence is still missing?"],
            "assumptions": ["The observation is incomplete."],
            "stop_conditions": ["Do not proceed without Human Gate review."],
        },
    )
    representation = to_structural_validation_representation(candidate)

    assert representation.candidate["intent"]["questions"] == [
        "What evidence is still missing?"
    ]
    assert representation.candidate["intent"]["assumptions"] == [
        "The observation is incomplete."
    ]
    assert representation.candidate["intent"]["stop_conditions"] == [
        "Do not proceed without Human Gate review."
    ]
    assert representation.candidate["origin"]["uncertainty"] == "unresolved"
    assert representation.candidate["approval"]["required"] is True
    assert representation.candidate["authority"] is False
    assert representation.candidate["executable"] is False
