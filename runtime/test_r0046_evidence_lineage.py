from evidence import capture_evidence
from landscape_adapter import InMemoryLandscapeAdapter
from prototype import Runtime, Transition


def lineage_protocol(context):
    state = dict(context.input["landscape"])
    return Transition(
        kind="evidence.lineage",
        data={
            "landscape_id": state["landscape_id"],
            "identity": state["identity"],
            "memory": state["memory"],
            "changed": True,
        },
    )


def test_same_landscape_state_preserves_distinct_evidence_provenance():
    landscape_a = InMemoryLandscapeAdapter(
        {
            "landscape_id": "landscape-003",
            "identity": "same-human-context",
            "memory": ["memory-004", "memory-005"],
        }
    )

    result_a = Runtime().execute(
        "lineage.protocol.a",
        lineage_protocol,
        {"landscape": landscape_a.read_state()},
    )
    evidence_a = capture_evidence(result_a)
    landscape_a.apply_transition(evidence_a)

    state_a = landscape_a.read_state()
    landscape_b = InMemoryLandscapeAdapter(state_a)

    result_b = Runtime().execute(
        "lineage.protocol.b",
        lineage_protocol,
        {"landscape": landscape_b.read_state()},
    )
    evidence_b = capture_evidence(result_b)
    landscape_b.apply_transition(evidence_b)

    state_b = landscape_b.read_state()

    assert state_b == state_a
    assert evidence_a.protocol_id == "lineage.protocol.a"
    assert evidence_b.protocol_id == "lineage.protocol.b"
    assert evidence_a.protocol_id != evidence_b.protocol_id
    assert evidence_a is not evidence_b


def test_equal_landscape_state_does_not_reconstruct_evidence_lineage():
    landscape_a = InMemoryLandscapeAdapter(
        {
            "landscape_id": "landscape-004",
            "identity": "same-human-context",
            "memory": ["memory-006"],
        }
    )

    result_a = Runtime().execute(
        "lineage.protocol.a",
        lineage_protocol,
        {"landscape": landscape_a.read_state()},
    )
    evidence_a = capture_evidence(result_a)
    landscape_a.apply_transition(evidence_a)

    state_a = landscape_a.read_state()
    landscape_b = InMemoryLandscapeAdapter(state_a)

    assert landscape_b.read_state() == state_a
    assert evidence_a.protocol_id == "lineage.protocol.a"
    assert evidence_a.transition_kind == "evidence.lineage"
