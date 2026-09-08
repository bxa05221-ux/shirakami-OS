from runtime.landscape import LandscapeState
from runtime.protocol_ir import ProtocolIR
from runtime.protocol_runtime import execute_protocol_ir
from runtime.prototype import Transition


def test_protocol_ir_reaches_runtime_and_produces_evidence():
    protocol_ir = ProtocolIR(
        protocol_id="writer-support",
        context_id="ctx-1",
        parent_landscape_ref="landscape-1",
        transition_kind="landscape.observation.appended",
        transition_data={"observation": "child chose a quiet corner", "changed": True},
    )

    def protocol(context):
        return Transition(
            kind=context.input["transition_kind"],
            data={**context.input["transition_data"]},
        )

    execution = execute_protocol_ir(protocol_ir, protocol)

    assert execution.result.status == "completed"
    assert execution.evidence.protocol_id == "writer-support"
    assert execution.evidence.transition_kind == "landscape.observation.appended"
    assert execution.evidence.transition_data["changed"] is True

    landscape = LandscapeState.empty()
    landscape.apply_evidence(execution.evidence)
    assert landscape.snapshot()["observation"] == "child chose a quiet corner"


def test_failed_execution_does_not_create_transition_evidence():
    protocol_ir = ProtocolIR(
        protocol_id="writer-support",
        context_id="ctx-1",
        parent_landscape_ref="landscape-1",
        transition_kind="landscape.observation.appended",
        transition_data={"observation": "should not apply"},
    )

    def failing_protocol(context):
        raise RuntimeError("not applied")

    execution = execute_protocol_ir(protocol_ir, failing_protocol)
    landscape = LandscapeState.empty()
    landscape.apply_evidence(execution.evidence)

    assert execution.result.status == "failed"
    assert landscape.snapshot() == {}
    assert landscape.evidence == []
