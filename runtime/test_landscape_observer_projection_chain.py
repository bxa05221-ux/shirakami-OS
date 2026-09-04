from evidence import capture_evidence
from landscape import LandscapeState
from prototype import Runtime, Transition
from projection import project_evidence
from replay import replay_landscape


def test_landscape_observer_projection_chain_replays_from_observed_state():
    runtime = Runtime()

    first = runtime.execute(
        "observer.landscape.initial",
        lambda context: Transition(
            kind="observer.landscape.initial",
            data={
                "place": context.input["place"],
                "visited": True,
                "changed": True,
            },
        ),
        {"place": "viewpoint"},
    )
    evidence_1 = capture_evidence(first)

    projected = LandscapeState.empty()
    project_evidence(evidence_1, projected)
    observed_state = projected.snapshot()

    second = runtime.execute(
        "observer.landscape.followup",
        lambda context: Transition(
            kind="observer.landscape.followup",
            data={
                "place": context.input["place"],
                "noticed": context.input["noticed"],
                "changed": True,
            },
        ),
        {"place": observed_state["place"], "noticed": "sunset"},
    )
    evidence_2 = capture_evidence(second)

    project_evidence(evidence_2, projected)
    replayed = replay_landscape([evidence_1, evidence_2])

    assert projected.snapshot() == {
        "place": "viewpoint",
        "visited": True,
        "noticed": "sunset",
        "changed": True,
    }
    assert replayed == projected.snapshot()
    assert evidence_1.transition_data["place"] == "viewpoint"
    assert "noticed" not in evidence_1.transition_data
