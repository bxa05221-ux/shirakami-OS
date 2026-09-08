from evidence import capture_evidence
from landscape import LandscapeState
from prototype import Runtime, Transition
from projection import project_evidence


def observed_with_external_interpretation(context):
    return Transition(
        kind="landscape.observation",
        data={
            "changed": True,
            "observed": context.input["observed"],
            "external_interpretation": context.input["external_interpretation"],
        },
    )


def test_interpretation_is_not_separately_owned_by_current_evidence_contract():
    result = Runtime().execute(
        "r0048.interpretation.boundary",
        observed_with_external_interpretation,
        {
            "observed": {"sound": "まだ不揃い"},
            "external_interpretation": "演奏者は不安だったのかもしれない",
        },
    )
    evidence = capture_evidence(result)

    assert evidence.transition_data["observed"] == {"sound": "まだ不揃い"}
    assert evidence.transition_data["external_interpretation"] == "演奏者は不安だったのかもしれない"
    assert not hasattr(evidence, "interpretation")
    assert evidence.confidence == "observed"


def test_projection_does_not_create_a_separate_interpretation_record():
    result = Runtime().execute(
        "r0048.interpretation.boundary",
        observed_with_external_interpretation,
        {
            "observed": {"sound": "最後まで演奏できた"},
            "external_interpretation": "自信がついたのかもしれない",
        },
    )
    evidence = capture_evidence(result)
    state = LandscapeState.empty()

    projected = project_evidence(evidence, state)

    assert projected["observed"] == {"sound": "最後まで演奏できた"}
    assert projected["external_interpretation"] == "自信がついたのかもしれない"
    assert len(state.evidence) == 1
    assert not hasattr(state.evidence[0], "interpretation")
