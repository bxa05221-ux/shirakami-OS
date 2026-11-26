import json
import pytest
from aiwitness.policy_gate import AIwitnessPolicyGate, OutboundPolicy, PolicyDenied
from runtime.openai_backend import OpenAIBackend

def allowed_gate():
    return AIwitnessPolicyGate(OutboundPolicy("policy-1", "1", True, frozenset({("openai", "test-model")}), frozenset({"public"})))
def test_openai_requires_gate_before_transport():
    called = False
    def transport(_):
        nonlocal called; called = True; return b"{}"
    with pytest.raises(PolicyDenied, match="policy gate"):
        OpenAIBackend("key", model="test-model", transport=transport).execute({"input":"safe", "data_classification":"public"})
    assert called is False
@pytest.mark.parametrize("classification", ["personal_information", "raw_evaluation_record", "confidential_context", "unknown", None])
def test_restricted_or_unclassified_input_never_reaches_openai(classification):
    called = False
    def transport(_):
        nonlocal called; called = True; return b"{}"
    with pytest.raises(PolicyDenied):
        OpenAIBackend("key", model="test-model", transport=transport, policy_gate=allowed_gate()).execute({"input":"secret", "data_classification":classification})
    assert called is False
def test_allowed_payload_is_fingerprinted_and_only_authorized_copy_is_sent():
    observed = []
    def transport(request):
        observed.append(json.loads(request.data.decode("utf-8"))); return b'{"id":"response"}'
    response = OpenAIBackend("key", model="test-model", transport=transport, policy_gate=allowed_gate()).execute({"input":{"summary":"public"}, "data_classification":"public"})
    assert response.payload["id"] == "response"
    assert observed == [{"model":"test-model", "input":{"summary":"public"}}]
def test_disabled_policy_fails_closed():
    disabled = AIwitnessPolicyGate(OutboundPolicy("policy-1", "1", False, frozenset(), frozenset()))
    with pytest.raises(PolicyDenied):
        OpenAIBackend("key", model="test-model", transport=lambda _: b"{}", policy_gate=disabled).execute({"input":"x", "data_classification":"public"})

def test_policy_exception_and_audit_do_not_copy_secret_payload():
    secret = "evaluation-secret-should-not-appear"
    gate = allowed_gate()
    with pytest.raises(PolicyDenied) as exc:
        gate.authorize({"input": secret, "data_classification": "personal_information"}, provider="openai", model="test-model")
    assert secret not in str(exc.value)
    assert secret not in repr(gate.audit.all())

def test_changed_authorized_payload_is_rejected_before_request():
    gate = allowed_gate()
    authorization = gate.authorize({"input": {"summary": "safe"}, "data_classification": "public"}, provider="openai", model="test-model")
    authorization.payload["summary"] = "changed"
    with pytest.raises(PolicyDenied, match="payload was changed"):
        gate.verify(authorization, provider="openai", model="test-model")
