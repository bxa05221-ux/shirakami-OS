from runtime.protocol_runtime_bridge import execute_protocol


def test_protocol_ir_executes_through_runtime():
    protocol = {
        "matome": {
            "title": "Bridge Test",
            "version": "0.1",
        }
    }

    execution = execute_protocol(protocol, lambda value: {"echo": value}, input_value="landscape")

    assert execution.protocol_title == "Bridge Test"
    assert execution.protocol_version == "0.1"
    assert execution.result.status == "success"
    assert execution.result.transition == "completed"
    assert execution.result.signals == [{"type": "execution.completed"}]


def test_protocol_ir_failure_is_preserved_as_runtime_result():
    protocol = {
        "matome": {
            "title": "Failure Test",
            "version": "0.1",
        }
    }

    def fail(_value):
        raise ValueError("expected failure")

    execution = execute_protocol(protocol, fail, input_value="landscape")

    assert execution.protocol_title == "Failure Test"
    assert execution.result.status == "failure"
    assert execution.result.transition == "failed"
    assert execution.result.signals == [{"type": "execution.failed", "error": "expected failure"}]
