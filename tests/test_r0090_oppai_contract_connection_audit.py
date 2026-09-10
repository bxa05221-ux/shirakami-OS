from collections.abc import Mapping

from examples.oppai_shirakami_api_minimal import ShirakamiRuntime
from runtime.evidence import capture_evidence
from runtime.landscape import LandscapeState
from runtime.protocol_api import ProtocolRequest, build_protocol_request, invoke_protocol
from runtime.protocol_registry import ProtocolRegistry
from runtime.protocol_runtime_bridge import execute_protocol
from runtime.projection import project_evidence
from runtime.prototype import Transition


def test_r0090_existing_contracts_form_downstream_vertical_path_without_oppai_entry_connection():
    registry = ProtocolRegistry()
    registry.register_default(
        "r0090.protocol",
        {"version": "0.1", "title": "R0090"},
    )

    request = build_protocol_request(
        registry,
        "r0090.protocol",
        {"raw_input": "hello r0090"},
    )
    assert isinstance(request, ProtocolRequest)
    assert request.protocol_id == "r0090.protocol"
    assert request.input == {"raw_input": "hello r0090"}

    observed_requests = []

    def executor(protocol_request):
        observed_requests.append(protocol_request)
        return execute_protocol(
            {
                "matome": {
                    "title": protocol_request.protocol_id,
                    "version": protocol_request.version or "",
                }
            },
            lambda _input: Transition(
                kind="r0090.transition",
                data={"changed": True, "input": dict(protocol_request.input)},
            ),
            input_value=protocol_request.input,
        )

    execution = invoke_protocol(request, executor)
    evidence = capture_evidence(execution.result)
    snapshot = project_evidence(evidence, LandscapeState.empty())

    assert observed_requests == [request]
    assert execution.result.status == "completed"
    assert evidence.protocol_id == "r0090.protocol"
    assert evidence.transition_data["input"] == {"raw_input": "hello r0090"}
    assert snapshot["last_transition"] == "r0090.transition"


def test_r0090_oppai_http_reference_entry_still_uses_only_existing_adapter_boundary():
    calls = []

    def adapter(input_text, context):
        calls.append((input_text, context))
        return "adapter-result"

    runtime = ShirakamiRuntime(adapter)
    result = runtime.chat("hello r0090", {"source": "human"}, "r0090")

    assert result["status"] == "ok"
    assert result["response"] == "adapter-result"
    assert calls == [("hello r0090", {"source": "human"})]
    assert result["context_delta"]["last_input"] == "hello r0090"


def test_r0090_oppai_evidence_metadata_is_not_an_evidence_record_contract():
    from runtime.oppai_runtime_flow import prepare

    prepared = prepare("hello r0090", protocol="default")

    assert isinstance(prepared.evidence, Mapping)
    assert prepared.evidence["schema"] == "OPPAI"
    assert "confidence" in prepared.evidence
    assert "protocol_id" not in prepared.evidence
    assert "transition_kind" not in prepared.evidence
