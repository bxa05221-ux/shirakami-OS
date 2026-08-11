from evidence import capture_evidence
from landscape_adapter import InMemoryLandscapeAdapter
from prototype import Runtime, example_protocol


def test_landscape_adapter_receives_verified_transition():
    result = Runtime().execute(
        "example.protocol",
        example_protocol,
        {"message": "adapter boundary"},
    )
    evidence = capture_evidence(result)

    adapter = InMemoryLandscapeAdapter()
    adapter.apply_transition(evidence)

    state = adapter.read_state()
    assert state["changed"] is True
    assert state["protocol_id"] == "example.protocol"


def test_landscape_adapter_does_not_apply_failure_as_transition():
    def failing_protocol(context):
        raise RuntimeError("boom")

    result = Runtime().execute("failing.protocol", failing_protocol, {})
    evidence = capture_evidence(result)

    adapter = InMemoryLandscapeAdapter()
    adapter.apply_transition(evidence)

    assert adapter.read_state() == {}
