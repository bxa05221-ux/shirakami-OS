from evidence import capture_evidence
from landscape_adapter import InMemoryLandscapeAdapter
from prototype import Runtime, Transition


def renderer_a(state):
    return {"renderer": "A", "landscape_id": state["landscape_id"], "identity": state["identity"]}


def renderer_b(state):
    return {"renderer": "B", "landscape_id": state["landscape_id"], "identity": state["identity"]}


def continuity_protocol(context):
    state = dict(context.input["landscape"])
    return Transition(
        kind="renderer.boundary.continuity",
        data={
            "landscape_id": state["landscape_id"],
            "identity": state["identity"],
            "memory": state["memory"],
            "changed": True,
        },
    )


def test_renderer_exchange_does_not_change_landscape_state():
    landscape = InMemoryLandscapeAdapter(
        {
            "landscape_id": "landscape-renderer-001",
            "identity": "same-landscape",
            "memory": ["memory-001", "memory-002"],
        }
    )

    result = Runtime().execute(
        "renderer.boundary.protocol",
        continuity_protocol,
        {"landscape": landscape.read_state()},
    )
    evidence = capture_evidence(result)
    landscape.apply_transition(evidence)

    state_before = landscape.read_state()
    rendered_a = renderer_a(state_before)
    rendered_b = renderer_b(state_before)
    state_after = landscape.read_state()

    assert rendered_a["landscape_id"] == rendered_b["landscape_id"]
    assert rendered_a["identity"] == rendered_b["identity"]
    assert state_after == state_before
    assert evidence.protocol_id == "renderer.boundary.protocol"


def test_renderer_exchange_is_not_evidence_reconstruction():
    landscape = InMemoryLandscapeAdapter(
        {
            "landscape_id": "landscape-renderer-002",
            "identity": "same-landscape",
            "memory": ["memory-003"],
        }
    )

    result = Runtime().execute(
        "renderer.boundary.protocol",
        continuity_protocol,
        {"landscape": landscape.read_state()},
    )
    evidence = capture_evidence(result)
    landscape.apply_transition(evidence)

    state = landscape.read_state()
    renderer_a(state)
    renderer_b(state)

    assert evidence.protocol_id == "renderer.boundary.protocol"
    assert evidence.transition_data
    assert evidence is not None
