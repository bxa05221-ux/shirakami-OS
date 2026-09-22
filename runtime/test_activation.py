import pytest

from runtime.activation import ActivationError, ActivationRequest, activate
from runtime.approval_envelope import ApprovalEnvelope


def _approved(protocol_id="protocol-1", candidate_id=None):
    envelope = ApprovalEnvelope(
        candidate_id=candidate_id or protocol_id,
        protocol_id=protocol_id,
    )
    return envelope.authorize_execution("human")


def test_activation_requires_explicit_authorization():
    envelope = ApprovalEnvelope("protocol-1", "protocol-1")

    with pytest.raises(ActivationError, match="explicit execution authorization"):
        ActivationRequest("protocol-1", envelope)


def test_activation_requires_matching_protocol():
    envelope = _approved("protocol-1")

    with pytest.raises(ActivationError, match="does not match protocol"):
        ActivationRequest("protocol-2", envelope)


def test_activation_rejects_unpromoted_candidate():
    envelope = _approved("protocol-1", candidate_id="candidate-1")

    with pytest.raises(ActivationError, match="promoted Approved Protocol"):
        ActivationRequest("protocol-1", envelope)


def test_activation_produces_observable_result():
    envelope = _approved("protocol-1")
    result = activate("protocol-1", envelope, context={"source": "human-gate"})

    assert result.protocol_id == "protocol-1"
    assert result.status == "activated"
    assert result.context == {"source": "human-gate"}
