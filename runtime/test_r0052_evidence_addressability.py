from evidence import capture_evidence
from landscape import LandscapeState
from prototype import Runtime, Transition


def addressable_protocol(context):
    return Transition(
        kind="landscape.observation",
        data={
            "changed": True,
            "observed": context.input["observed"],
            "external_interpretation": context.input["external_interpretation"],
        },
    )


def test_multiple_evidence_records_remain_addressable_in_landscape_state():
    state = LandscapeState.empty()
    shared_payload = "同じ解釈らしき値"

    result_a = Runtime().execute(
        "r0052.protocol.a",
        addressable_protocol,
        {
            "observed": {"scene": "A"},
            "external_interpretation": shared_payload,
        },
    )
    evidence_a = capture_evidence(result_a)

    result_b = Runtime().execute(
        "r0052.protocol.b",
        addressable_protocol,
        {
            "observed": {"scene": "B"},
            "external_interpretation": shared_payload,
        },
    )
    evidence_b = capture_evidence(result_b)

    state.apply_evidence(evidence_a)
    state.apply_evidence(evidence_b)

    assert len(state.evidence) == 2
    assert state.evidence[0] is evidence_a
    assert state.evidence[1] is evidence_b
    assert state.evidence[0].protocol_id == "r0052.protocol.a"
    assert state.evidence[1].protocol_id == "r0052.protocol.b"
    assert state.evidence[0].transition_data["external_interpretation"] == shared_payload
    assert state.evidence[1].transition_data["external_interpretation"] == shared_payload


def test_current_landscape_snapshot_is_not_evidence_lineage():
    state = LandscapeState.empty()
    result = Runtime().execute(
        "r0052.protocol.snapshot",
        addressable_protocol,
        {
            "observed": {"scene": "snapshot"},
            "external_interpretation": "状態として見える値",
        },
    )
    evidence = capture_evidence(result)
    state.apply_evidence(evidence)

    snapshot = state.snapshot()

    assert snapshot["observed"] == {"scene": "snapshot"}
    assert snapshot["external_interpretation"] == "状態として見える値"
    assert len(state.evidence) == 1
    assert state.evidence[0] is evidence
    assert state.evidence[0].protocol_id == "r0052.protocol.snapshot"
