import pytest

from runtime.approval_envelope import ApprovalEnvelope, ApprovalEnvelopeError


def test_envelope_starts_without_authorization():
    envelope = ApprovalEnvelope("candidate-1", "protocol-1")
    assert not envelope.execution_authorized
    assert not envelope.publication_authorized


def test_execution_requires_reviewer():
    with pytest.raises(ApprovalEnvelopeError):
        ApprovalEnvelope("candidate-1", "protocol-1", execution_authorized=True)


def test_publication_cannot_be_granted_without_execution():
    envelope = ApprovalEnvelope("candidate-1", "protocol-1")
    with pytest.raises(ApprovalEnvelopeError):
        envelope.authorize_publication("human-1")


def test_authorization_is_explicit_and_immutable():
    envelope = ApprovalEnvelope("candidate-1", "protocol-1")
    approved = envelope.authorize_execution("human-1")
    assert not envelope.execution_authorized
    assert approved.execution_authorized
    assert not approved.publication_authorized


def test_publication_requires_publication_scope():
    envelope = ApprovalEnvelope("candidate-1", "protocol-1").authorize_execution("human-1")
    with pytest.raises(ApprovalEnvelopeError):
        envelope.authorize_publication("human-1")


def test_publication_is_separate_explicit_step():
    envelope = ApprovalEnvelope("candidate-1", "protocol-1").authorize_execution(
        "human-1", scope="publication"
    )
    published = envelope.authorize_publication("human-1")
    assert published.execution_authorized
    assert published.publication_authorized
