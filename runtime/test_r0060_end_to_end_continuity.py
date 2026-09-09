from evidence import capture_evidence
from landscape_adapter import InMemoryLandscapeAdapter
from prototype import Runtime, Transition


def continuity_protocol(context):
    state = dict(context.input["landscape"])
    return Transition(
        kind="continuity.end_to_end",
        data={
            "landscape_id": state["landscape_id"],
            "identity": state["identity"],
            "memory": list(state["memory"]),
            "observed": True,
        },
    )


def renderer(label, state):
    return {
        "renderer": label,
        "landscape_id": state["landscape_id"],
        "identity": state["identity"],
        "memory": list(state["memory"]),
    }


def test_adapter_and_renderer_exchange_preserve_landscape_continuity():
    landscape_a = InMemoryLandscapeAdapter(
        {
            "landscape_id": "landscape-r0060",
            "identity": "same-context",
            "memory": ["memory-001", "memory-002"],
        }
    )

    result_a = Runtime().execute(
        "continuity.end_to_end.a",
        continuity_protocol,
        {"landscape": landscape_a.read_state()},
    )
    evidence_a = capture_evidence(result_a)
    landscape_a.apply_transition(evidence_a)
    state_after_a = landscape_a.read_state()

    landscape_b = InMemoryLandscapeAdapter(state_after_a)
    result_b = Runtime().execute(
        "continuity.end_to_end.b",
        continuity_protocol,
        {"landscape": landscape_b.read_state()},
    )
    evidence_b = capture_evidence(result_b)
    landscape_b.apply_transition(evidence_b)
    state_after_b = landscape_b.read_state()

    rendered_a = renderer("A", state_after_b)
    rendered_b = renderer("B", state_after_b)

    assert state_after_b == landscape_b.read_state()
    assert rendered_a["landscape_id"] == rendered_b["landscape_id"]
    assert rendered_a["identity"] == rendered_b["identity"]
    assert rendered_a["memory"] == rendered_b["memory"]
    assert evidence_a.protocol_id == "continuity.end_to_end.a"
    assert evidence_b.protocol_id == "continuity.end_to_end.b"


def test_adapter_and_renderer_exchange_keep_evidence_independent():
    landscape = InMemoryLandscapeAdapter(
        {
            "landscape_id": "landscape-r0060-evidence",
            "identity": "same-context",
            "memory": ["memory-003"],
        }
    )

    result = Runtime().execute(
        "continuity.end_to_end.evidence",
        continuity_protocol,
        {"landscape": landscape.read_state()},
    )
    evidence = capture_evidence(result)
    landscape.apply_transition(evidence)

    state = landscape.read_state()
    renderer("A", state)
    renderer("B", state)

    assert evidence.protocol_id == "continuity.end_to_end.evidence"
    assert evidence.transition_data
    assert landscape.read_state() == state
