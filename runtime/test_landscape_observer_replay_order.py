from evidence import capture_evidence
from landscape import LandscapeState
from prototype import Runtime, Transition
from projection import project_evidence
from replay import replay_landscape


def _evidence(runtime, protocol_id, place, **data):
    result = runtime.execute(
        protocol_id,
        lambda context: Transition(
            kind=protocol_id,
            data={"place": context.input["place"], **data, "changed": True},
        ),
        {"place": place},
    )
    return capture_evidence(result)


def test_landscape_observer_replay_preserves_evidence_order():
    runtime = Runtime()
    evidence_1 = _evidence(runtime, "observer.landscape.first", "viewpoint", phase="first")
    evidence_2 = _evidence(runtime, "observer.landscape.second", "harbor", phase="second")

    forward = replay_landscape([evidence_1, evidence_2])
    reverse = replay_landscape([evidence_2, evidence_1])

    assert forward == {"place": "harbor", "phase": "second", "changed": True}
    assert reverse == {"place": "viewpoint", "phase": "first", "changed": True}
    assert forward != reverse

    sequential_forward = LandscapeState.empty()
    project_evidence(evidence_1, sequential_forward)
    project_evidence(evidence_2, sequential_forward)
    assert forward == sequential_forward.snapshot()
