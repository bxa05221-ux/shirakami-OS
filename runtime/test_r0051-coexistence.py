from evidence import capture_evidence
from landscape_adapter import InMemoryLandscapeAdapter
from prototype import Runtime, Transition


def provenance_protocol(context):
    return Transition(
        kind="landscape.observation",
        data={
            "changed": True,
            "observed": context.input["observed"],
            "external_interpretation": context.input["external_interpretation"],
        },
    )


def test_distinct_provenance_can_coexist_in_one_landscape_without_inference():
    adapter = InMemoryLandscapeAdapter()
    shared_payload = "同じ解釈らしき値"

    result_a = Runtime().execute(
        "r0051.protocol.a",
        provenance_protocol,
        {
            "observed": {"scene": "A"},
            "external_interpretation": shared_payload,
        },
    )
    evidence_a = capture_evidence(result_a)

    result_b = Runtime().execute(
        "r0051.protocol.b",
        provenance_protocol,
        {
            "observed": {"scene": "B"},
            "external_interpretation": shared_payload,
        },
    )
    evidence_b = capture_evidence(result_b)

    assert evidence_a is not evidence_b
    assert evidence_a.protocol_id != evidence_b.protocol_id
    assert evidence_a.transition_data["external_interpretation"] == shared_payload
    assert evidence_b.transition_data["external_interpretation"] == shared_payload

    adapter.apply_transition(evidence_a)
    state_after_a = adapter.read_state()
    adapter.apply_transition(evidence_b)
    state_after_b = adapter.read_state()

    assert state_after_a["external_interpretation"] == shared_payload
    assert state_after_b["external_interpretation"] == shared_payload
    assert state_after_a["observed"] == {"scene": "A"}
    assert state_after_b["observed"] == {"scene": "B"}


def test_adapter_state_does_not_rewrite_evidence_provenance():
    adapter = InMemoryLandscapeAdapter()
    shared_payload = "同じ解釈らしき値"

    result_a = Runtime().execute(
        "r0051.protocol.a",
        provenance_protocol,
        {"observed": {"scene": "A"}, "external_interpretation": shared_payload},
    )
    evidence_a = capture_evidence(result_a)
    adapter.apply_transition(evidence_a)

    result_b = Runtime().execute(
        "r0051.protocol.b",
        provenance_protocol,
        {"observed": {"scene": "B"}, "external_interpretation": shared_payload},
    )
    evidence_b = capture_evidence(result_b)
    adapter.apply_transition(evidence_b)

    assert evidence_a.protocol_id == "r0051.protocol.a"
    assert evidence_b.protocol_id == "r0051.protocol.b"
    assert evidence_a.transition_data["external_interpretation"] == evidence_b.transition_data["external_interpretation"]
