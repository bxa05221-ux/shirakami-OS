from evidence import capture_evidence
from landscape_adapter import InMemoryLandscapeAdapter
from prototype import Runtime, Transition


def continuity_protocol(context):
    state = dict(context.input["landscape"])
    return Transition(
        kind="landscape.continuity",
        data={
            "landscape_id": state["landscape_id"],
            "identity": state["identity"],
            "memory": state["memory"],
            "changed": True,
            "continuity_check": True,
        },
    )


def test_landscape_continuity_survives_runtime_and_adapter_exchange():
    landscape_a = InMemoryLandscapeAdapter(
        {
            "landscape_id": "landscape-001",
            "identity": "same-human-context",
            "memory": ["memory-001", "memory-002"],
        }
    )

    result_a = Runtime().execute(
        "continuity.protocol.a",
        continuity_protocol,
        {"landscape": landscape_a.read_state()},
    )
    evidence_a = capture_evidence(result_a)
    landscape_a.apply_transition(evidence_a)

    state_before_exchange = landscape_a.read_state()
    landscape_b = InMemoryLandscapeAdapter(state_before_exchange)

    result_b = Runtime().execute(
        "continuity.protocol.b",
        continuity_protocol,
        {"landscape": landscape_b.read_state()},
    )
    evidence_b = capture_evidence(result_b)
    landscape_b.apply_transition(evidence_b)

    state_after_exchange = landscape_b.read_state()

    assert state_after_exchange["landscape_id"] == state_before_exchange["landscape_id"]
    assert state_after_exchange["identity"] == state_before_exchange["identity"]
    assert state_after_exchange["memory"] == state_before_exchange["memory"]
    assert state_after_exchange["continuity_check"] is True
    assert evidence_a.protocol_id == "continuity.protocol.a"
    assert evidence_b.protocol_id == "continuity.protocol.b"
    assert evidence_a is not evidence_b


def test_landscape_continuity_does_not_equate_state_with_evidence_lineage():
    landscape_a = InMemoryLandscapeAdapter(
        {
            "landscape_id": "landscape-002",
            "identity": "same-human-context",
            "memory": ["memory-003"],
        }
    )

    result_a = Runtime().execute(
        "continuity.protocol.a",
        continuity_protocol,
        {"landscape": landscape_a.read_state()},
    )
    evidence_a = capture_evidence(result_a)
    landscape_a.apply_transition(evidence_a)

    landscape_b = InMemoryLandscapeAdapter(landscape_a.read_state())

    assert landscape_b.read_state() == landscape_a.read_state()
    assert evidence_a.protocol_id == "continuity.protocol.a"
    assert evidence_a.transition_data
