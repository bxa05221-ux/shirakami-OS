from evidence import capture_evidence
from landscape_adapter import InMemoryLandscapeAdapter
from prototype import Runtime, Transition


def external_interpretation_protocol(context):
    return Transition(
        kind="landscape.observation",
        data={
            "changed": True,
            "observed": context.input["observed"],
            "external_interpretation": context.input["external_interpretation"],
        },
    )


def test_same_payload_does_not_equate_evidence_provenance():
    interpretation = "誰かを待っていたのかもしれない"

    result_a = Runtime().execute(
        "r0050.protocol.a",
        external_interpretation_protocol,
        {
            "observed": {"scene": "雨のあと"},
            "external_interpretation": interpretation,
        },
    )
    result_b = Runtime().execute(
        "r0050.protocol.b",
        external_interpretation_protocol,
        {
            "observed": {"scene": "雨のあと"},
            "external_interpretation": interpretation,
        },
    )

    evidence_a = capture_evidence(result_a)
    evidence_b = capture_evidence(result_b)

    assert evidence_a is not evidence_b
    assert evidence_a.protocol_id == "r0050.protocol.a"
    assert evidence_b.protocol_id == "r0050.protocol.b"
    assert evidence_a.protocol_id != evidence_b.protocol_id
    assert evidence_a.transition_data["external_interpretation"] == interpretation
    assert evidence_b.transition_data["external_interpretation"] == interpretation


def test_same_payload_remains_distinct_after_landscape_adapter_boundary():
    interpretation = "別れを惜しんでいたのかもしれない"
    adapter_a = InMemoryLandscapeAdapter()
    adapter_b = InMemoryLandscapeAdapter()

    result_a = Runtime().execute(
        "r0050.protocol.a",
        external_interpretation_protocol,
        {
            "observed": {"scene": "駅前"},
            "external_interpretation": interpretation,
        },
    )
    result_b = Runtime().execute(
        "r0050.protocol.b",
        external_interpretation_protocol,
        {
            "observed": {"scene": "駅前"},
            "external_interpretation": interpretation,
        },
    )

    evidence_a = capture_evidence(result_a)
    evidence_b = capture_evidence(result_b)
    adapter_a.apply_transition(evidence_a)
    adapter_b.apply_transition(evidence_b)

    state_a = adapter_a.read_state()
    state_b = adapter_b.read_state()

    assert state_a["external_interpretation"] == state_b["external_interpretation"]
    assert evidence_a.protocol_id != evidence_b.protocol_id
    assert evidence_a is not evidence_b
