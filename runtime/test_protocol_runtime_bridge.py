from runtime.protocol_runtime_bridge import execute_protocol
from runtime.prototype import Transition


def test_protocol_ir_executes_through_runtime():
    protocol = {
        "matome": {
            "title": "Bridge Test",
            "version": "0.1",
        }
    }

    def transition(value):
        return Transition(kind="bridge.echo", data={"echo": value})

    execution = execute_protocol(protocol, transition, input_value={"landscape": "external-test"})

    assert execution.protocol_title == "Bridge Test"
    assert execution.protocol_version == "0.1"
    assert execution.result.status == "completed"
    assert execution.result.transition.kind == "bridge.echo"
    assert execution.result.transition.data == {"echo": {"landscape": "external-test"}}
    assert execution.result.signals == ("execution.completed", "transition.observed")


def test_protocol_ir_failure_is_preserved_as_runtime_result():
    protocol = {
        "matome": {
            "title": "Failure Test",
            "version": "0.1",
        }
    }

    def fail(_value):
        raise ValueError("expected failure")

    execution = execute_protocol(protocol, fail, input_value={"landscape": "external-test"})

    assert execution.protocol_title == "Failure Test"
    assert execution.result.status == "failed"
    assert execution.result.transition.kind == "execution.failed"
    assert execution.result.transition.data["error_type"] == "ValueError"
    assert execution.result.transition.data["message"] == "expected failure"
    assert execution.result.signals == ("execution.failed", "transition.observed")
