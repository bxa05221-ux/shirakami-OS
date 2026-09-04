from evidence import capture_evidence
from landscape import LandscapeState
from prototype import Runtime, Transition
from replay import replay_landscape


def initial_transition(context):
    return Transition(
        kind="observer.landscape.initial",
        data={
            "place": context.input["place"],
            "visited": True,
            "changed": True,
        },
    )


def followup_transition(context):
    return Transition(
        kind="observer.landscape.followup",
        data={
            "place": context.input["place"],
            "noticed": context.input["noticed"],
            "changed": True,
        },
    )


def test_landscape_observer_replay_preserves_evidence_boundary():
    runtime = Runtime()

    first_result = runtime.execute(
        "observer.landscape.initial",
        initial_transition,
        {"place": "viewpoint"},
    )
    evidence_1 = capture_evidence(first_result)

    projected = LandscapeState.empty()
    projected.apply_evidence(evidence_1)
    observed_state = projected.snapshot()

    second_result = runtime.execute(
        "observer.landscape.followup",
        followup_transition,
        {
            "place": observed_state["place"],
            "noticed": "sunset",
        },
    )
    evidence_2 = capture_evidence(second_result)

    assert evidence_1.transition_kind == "observer.landscape.initial"
    assert evidence_1.transition_data["visited"] is True
    assert evidence_2.transition_kind == "observer.landscape.followup"
    assert evidence_2.transition_data["noticed"] == "sunset"

    replayed = replay_landscape([evidence_1, evidence_2])

    assert replayed == {
        "place": "viewpoint",
        "visited": True,
        "noticed": "sunset",
        "changed": True,
    }
    assert evidence_1.transition_data["visited"] is True
    assert "noticed" not in evidence_1.transition_data
