import pytest

from runtime.approval_envelope import ApprovalEnvelope, ApprovalEnvelopeError


def test_nested_context_is_immutable():
    envelope = ApprovalEnvelope(
        candidate_id="candidate-1",
        protocol_id="protocol-1",
        context={"nested": {"items": ["evidence-1"]}},
    )
    with pytest.raises(TypeError):
        envelope.context["nested"]["items"] = ("tampered",)


def test_publication_requires_same_reviewer():
    approved = ApprovalEnvelope(
        candidate_id="candidate-1", protocol_id="protocol-1"
    ).authorize_execution("reviewer-1", scope="publication")
    with pytest.raises(ApprovalEnvelopeError):
        approved.authorize_publication("reviewer-2")


def test_publication_requires_nonempty_reviewer():
    approved = ApprovalEnvelope(
        candidate_id="candidate-1", protocol_id="protocol-1"
    ).authorize_execution("reviewer-1", scope="publication")
    with pytest.raises(ApprovalEnvelopeError):
        approved.authorize_publication("")
