from evidence import capture_evidence
from prototype import Runtime, Transition


def tabitomo_protocol(context):
    choice = context.input["traveler_choice"]
    return Transition(
        kind="tabitomo.choice.observed",
        data={
            "character_response": "千鶴なら、こちらの道も面白いと思うよ。",
            "options_presented": ["quiet_route", "scenic_route"],
            "traveler_choice": choice,
            "changed": True,
        },
    )


def tabitomo_outcome_protocol(context):
    return Transition(
        kind="tabitomo.outcome.observed",
        data={
            "traveler_choice": context.input["traveler_choice"],
            "observed_outcome": context.input["observed_outcome"],
            "changed": True,
        },
    )


def test_tabitomo_preserves_human_choice_before_evidence():
    runtime = Runtime()
    result = runtime.execute(
        "tabitomo.human_choice",
        tabitomo_protocol,
        {"traveler_choice": "scenic_route"},
    )

    assert result.status == "completed"
    assert result.transition.data["traveler_choice"] == "scenic_route"
    assert result.transition.data["options_presented"] == ["quiet_route", "scenic_route"]

    evidence = capture_evidence(result)
    assert evidence.transition_kind == "tabitomo.choice.observed"
    assert evidence.transition_data["traveler_choice"] == "scenic_route"
    assert evidence.transition_data["character_response"] != "scenic_route"


def test_tabitomo_character_does_not_become_the_decision():
    runtime = Runtime()
    result = runtime.execute(
        "tabitomo.human_choice",
        tabitomo_protocol,
        {"traveler_choice": "quiet_route"},
    )

    assert result.transition.data["traveler_choice"] == "quiet_route"
    assert result.transition.data["character_response"].startswith("千鶴なら")
    assert result.transition.data["character_response"] != result.transition.data["traveler_choice"]


def test_tabitomo_choice_is_not_itself_an_observed_outcome():
    runtime = Runtime()
    choice_result = runtime.execute(
        "tabitomo.human_choice",
        tabitomo_protocol,
        {"traveler_choice": "scenic_route"},
    )
    outcome_result = runtime.execute(
        "tabitomo.outcome",
        tabitomo_outcome_protocol,
        {
            "traveler_choice": "scenic_route",
            "observed_outcome": "arrived_at_viewpoint",
        },
    )

    choice_evidence = capture_evidence(choice_result)
    outcome_evidence = capture_evidence(outcome_result)

    assert choice_evidence.transition_kind == "tabitomo.choice.observed"
    assert choice_evidence.transition_data["traveler_choice"] == "scenic_route"
    assert "observed_outcome" not in choice_evidence.transition_data

    assert outcome_evidence.transition_kind == "tabitomo.outcome.observed"
    assert outcome_evidence.transition_data["traveler_choice"] == "scenic_route"
    assert outcome_evidence.transition_data["observed_outcome"] == "arrived_at_viewpoint"
