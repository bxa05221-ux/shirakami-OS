from evidence import capture_evidence
from landscape_adapter import InMemoryLandscapeAdapter
from prototype import Runtime, example_protocol


def test_multi_protocol_landscape_preserves_protocol_provenance():
    result_a = Runtime().execute(
        "protocol.a",
        example_protocol,
        {"message": "protocol A"},
    )
    result_b = Runtime().execute(
        "protocol.b",
        example_protocol,
        {"message": "protocol B"},
    )

    evidence_a = capture_evidence(result_a)
    evidence_b = capture_evidence(result_b)

    adapter = InMemoryLandscapeAdapter()
    adapter.apply_transition(evidence_a)
    state_after_a = adapter.read_state()
    adapter.apply_transition(evidence_b)
    state_after_b = adapter.read_state()

    assert evidence_a.protocol_id == "protocol.a"
    assert evidence_b.protocol_id == "protocol.b"
    assert evidence_a is not evidence_b
    assert state_after_a["protocol_id"] == "protocol.a"
    assert state_after_b["protocol_id"] == "protocol.b"
