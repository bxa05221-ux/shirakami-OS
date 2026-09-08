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


def test_external_interpretation_remains_payload_with_protocol_provenance():
    adapter = InMemoryLandscapeAdapter()
    result = Runtime().execute(
        "r0049.interpretation.provenance",
        external_interpretation_protocol,
        {
            "observed": {"scene": "雨のあと"},
            "external_interpretation": "誰かを待っていたのかもしれない",
        },
    )
    evidence = capture_evidence(result)
    adapter.apply_transition(evidence)

    state = adapter.read_state()

    assert state["observed"] == {"scene": "雨のあと"}
    assert state["external_interpretation"] == "誰かを待っていたのかもしれない"
    assert evidence.protocol_id == "r0049.interpretation.provenance"
    assert not hasattr(evidence, "interpretation")


def test_interpretation_payload_does_not_change_evidence_provenance():
    result = Runtime().execute(
        "r0049.interpretation.provenance",
        external_interpretation_protocol,
        {
            "observed": {"scene": "駅前"},
            "external_interpretation": "別れを惜しんでいたのかもしれない",
        },
    )
    evidence = capture_evidence(result)

    assert evidence.protocol_id == "r0049.interpretation.provenance"
    assert evidence.transition_kind == "landscape.observation"
    assert evidence.transition_data["external_interpretation"] == "別れを惜しんでいたのかもしれない"
    assert evidence.confidence == "observed"
