from evidence import capture_evidence
from landscape import LandscapeState
from prototype import Runtime, Transition
from projection import project_evidence
from replay import replay_landscape


def test_landscape_observer_replay_matches_sequential_observed_projection():
    runtime = Runtime()

    first = runtime.execute(
        "observer.landscape.initial",
        lambda context: Transition(
            kind="observer.landscape.initial",
            data={"place": context.input["place"], "visited": True, "changed": True},
        ),
        {"place": "viewpoint"},
    )
    evidence_1 = capture_evidence(first)

    sequential = LandscapeState.empty()
    project_evidence(evidence_1, sequential)
    observed_state = sequential.snapshot()

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
    project_evidence(evidence_2, sequential)

    replayed = replay_landscape([evidence_1, evidence_2])

    assert replayed == sequential.snapshot()
    assert replayed == {
        "place": "viewpoint",
        "visited": True,
        "noticed": "sunset",
        "changed": True,
    }
