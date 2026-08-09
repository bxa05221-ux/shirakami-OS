from prototype import Runtime, Transition, example_protocol


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
