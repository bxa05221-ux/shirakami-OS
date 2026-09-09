from runtime.evidence import capture_evidence
from runtime.landscape import LandscapeState
from runtime.protocol_api import ProtocolRequest, invoke_protocol
from runtime.protocol_runtime_bridge import execute_protocol
from runtime.prototype import Transition


def test_protocol_request_runtime_bridge_to_evidence_landscape():
    request = ProtocolRequest(
        protocol_id="r0088.protocol",
        version="0.1",
        input={"message": "hello r0088"},
    )

    execution = invoke_protocol(
        request,
        lambda protocol_request: execute_protocol(
            {
                "matome": {
                    "title": protocol_request.protocol_id,
                    "version": protocol_request.version or "",
                }
            },
            lambda input_data: Transition(
                kind="r0088.transition",
                data={
                    "input": dict(input_data),
                    "changed": True,
                },
            ),
            input_value=protocol_request.input,
        ),
    )

    evidence = capture_evidence(execution.result)
    landscape = LandscapeState.empty()
    landscape.apply_evidence(evidence)

    assert execution.protocol_title == request.protocol_id
    assert execution.protocol_version == request.version
    assert execution.result.status == "completed"
    assert evidence.protocol_id == request.protocol_id
    assert evidence.transition_data["input"] == dict(request.input)
    assert landscape.snapshot()["input"] == dict(request.input)
    assert landscape.evidence == [evidence]
