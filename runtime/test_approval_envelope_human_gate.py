import pytest

from runtime.approval_envelope import ApprovalEnvelope, ApprovalEnvelopeError


def test_candidate_metadata_crosses_boundary_without_authorization():
    envelope = ApprovalEnvelope(
        candidate_id="route-candidate-1",
        protocol_id="protocol-1",
        provenance=("oppai", "human_gate"),
        evidence_ids=("evidence-1",),
    )

    assert envelope.candidate_id == "route-candidate-1"
    assert envelope.protocol_id == "protocol-1"
    assert envelope.provenance == ("oppai", "human_gate")
    assert envelope.evidence_ids == ("evidence-1",)
    assert not envelope.execution_authorized
    assert not envelope.publication_authorized


def test_human_gate_authorizes_execution_without_publication():
    envelope = ApprovalEnvelope(
        candidate_id="route-candidate-1",
        protocol_id="protocol-1",
        provenance=("oppai", "human_gate"),
    )

    approved = envelope.authorize_execution("human-reviewer-1")

    assert approved.execution_authorized
    assert not approved.publication_authorized
    assert approved.provenance == envelope.provenance
    assert approved.candidate_id == envelope.candidate_id
    assert approved.protocol_id == envelope.protocol_id


def test_publication_requires_explicit_publication_scope():
    approved = ApprovalEnvelope(
        candidate_id="route-candidate-1",
        protocol_id="protocol-1",
    ).authorize_execution("human-reviewer-1")

    with pytest.raises(ApprovalEnvelopeError):
        approved.authorize_publication("human-reviewer-1")


def test_unauthorized_candidate_cannot_become_authorized_implicitly():
    envelope = ApprovalEnvelope("route-candidate-1", "protocol-1")

    assert envelope.execution_authorized is False
    assert envelope.publication_authorized is False
