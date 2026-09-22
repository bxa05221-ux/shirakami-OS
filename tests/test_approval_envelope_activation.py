import pytest

from runtime.approval_envelope import ApprovalEnvelope
from runtime.approval_envelope_activation import to_activation_input


def authorized_envelope():
    return ApprovalEnvelope(
        candidate_id="candidate-001",
        protocol_id="protocol-001",
        provenance=("observation-001",),
        evidence_ids=("evidence-001",),
    ).authorize_execution("reviewer-001")


def test_explicit_envelope_metadata_maps_to_activation_input():
    result = to_activation_input(authorized_envelope())

    assert result["candidate_id"] == "candidate-001"
    assert result["protocol_id"] == "protocol-001"
    assert result["reviewer"] == "reviewer-001"
    assert result["provenance"] == ("observation-001",)
    assert result["evidence_ids"] == ("evidence-001",)
    assert result["execution_authorized"] is True
    assert result["approval_scope"] == "execution"


def test_unapproved_envelope_fails_closed():
    envelope = ApprovalEnvelope(
        candidate_id="candidate-001",
        protocol_id="protocol-001",
    )

    with pytest.raises(ValueError):
        to_activation_input(envelope)


def test_missing_reviewer_fails_closed():
    envelope = ApprovalEnvelope(
        candidate_id="candidate-001",
        protocol_id="protocol-001",
        execution_authorized=False,
    )

    with pytest.raises(ValueError):
        to_activation_input(envelope)


def test_non_envelope_input_fails_closed():
    with pytest.raises(TypeError):
        to_activation_input({
            "candidate_id": "candidate-001",
            "protocol_id": "protocol-001",
        })
