from evidence import capture_evidence
from landscape import LandscapeState
from prototype import Runtime, example_protocol


def test_transition_updates_landscape_without_mutating_evidence():
    result = Runtime().execute(
        "example.protocol",
        example_protocol,
        {"message": "hello landscape"},
    )
    evidence = capture_evidence(result)
    before = dict(evidence.transition_data)

    landscape = LandscapeState.empty()
    assert landscape.snapshot() == {}

    landscape.apply_evidence(evidence)

    assert landscape.snapshot()["changed"] is True
    assert landscape.snapshot()["protocol_id"] == "example.protocol"
    assert dict(evidence.transition_data) == before


def test_failure_evidence_does_not_change_landscape():
    def failing_protocol(context):
        raise RuntimeError("boom")

    result = Runtime().execute("failing.protocol", failing_protocol, {})
    evidence = capture_evidence(result)

    landscape = LandscapeState.empty()
    landscape.apply_evidence(evidence)

    assert landscape.snapshot() == {}
