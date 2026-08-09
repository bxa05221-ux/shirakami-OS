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
