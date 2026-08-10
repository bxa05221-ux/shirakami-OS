from prototype import Runtime, Transition, example_protocol, failing_protocol


def test_minimal_vertical_slice():
    runtime = Runtime()

    result = runtime.execute(
        "example.protocol",
        example_protocol,
        {"message": "hello landscape"},
    )

    assert result.status == "completed"
    assert result.protocol_id == "example.protocol"
    assert isinstance(result.transition, Transition)
    assert result.transition.kind == "example.transition"
    assert result.transition.data["changed"] is True
    assert "execution.completed" in result.signals
    assert "transition.observed" in result.signals


def test_failure_is_observable():
    runtime = Runtime()

    result = runtime.execute(
        "failing.protocol",
        failing_protocol,
        {"message": "trigger failure"},
    )

    assert result.status == "failed"
    assert result.protocol_id == "failing.protocol"
    assert result.transition.kind == "execution.failed"
    assert result.transition.data["error_type"] == "RuntimeError"
    assert result.transition.data["message"] == "intentional prototype failure"
    assert "execution.failed" in result.signals
    assert "transition.observed" in result.signals


def test_invalid_protocol_id_is_observable():
    runtime = Runtime()

    result = runtime.execute("", example_protocol, {})

    assert result.status == "failed"
    assert result.transition.kind == "execution.invalid_input"
    assert result.transition.data["error_type"] == "InvalidProtocolId"
    assert "execution.invalid" in result.signals


def test_invalid_protocol_is_observable():
    runtime = Runtime()

    result = runtime.execute("invalid.protocol", None, {})

    assert result.status == "failed"
    assert result.transition.kind == "execution.invalid_input"
    assert result.transition.data["error_type"] == "InvalidProtocol"
    assert "execution.invalid" in result.signals


def test_invalid_context_input_is_observable():
    runtime = Runtime()

    result = runtime.execute("invalid.context", example_protocol, ["not", "a", "mapping"])

    assert result.status == "failed"
    assert result.transition.kind == "execution.invalid_input"
    assert result.transition.data["error_type"] == "InvalidContextInput"
    assert "execution.invalid" in result.signals


def test_invalid_protocol_result_is_observable():
    runtime = Runtime()

    def bad_protocol(context):
        return {"changed": True}

    result = runtime.execute("bad.result", bad_protocol, {})

    assert result.status == "failed"
    assert result.transition.kind == "execution.invalid_result"
    assert result.transition.data["error_type"] == "InvalidProtocolResult"
    assert "execution.invalid" in result.signals
