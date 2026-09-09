from runtime.default_protocol import bootstrap_default_protocol
from runtime.evidence import capture_evidence
from runtime.landscape import LandscapeState
from runtime.protocol_api import build_protocol_request, invoke_protocol
from runtime.protocol_registry import ProtocolRegistry
from runtime.prototype import Runtime, example_protocol


def test_protocol_api_to_runtime_evidence_landscape_path():
    registry = ProtocolRegistry()
    bootstrap_default_protocol(registry)

    request = build_protocol_request(
        registry,
        request_protocol_id := registry.require_default().protocol_id,
        {"message": "hello landscape"},
    )

    result = invoke_protocol(
        request,
        lambda protocol_request: Runtime().execute(
            protocol_request.protocol_id,
            example_protocol,
            protocol_request.input,
        ),
    )
    evidence = capture_evidence(result)
    landscape = LandscapeState.empty()
    landscape.apply_evidence(evidence)

    assert request.protocol_id == request_protocol_id
    assert result.status == "completed"
    assert evidence.protocol_id == request.protocol_id
    assert evidence.transition_data["input"] == {"message": "hello landscape"}
    assert landscape.snapshot()["input"] == {"message": "hello landscape"}
    assert landscape.evidence == [evidence]
