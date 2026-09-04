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


def test_landscape_observer_preserves_multi_stage_evidence_history():
    runtime = Runtime()

    evidence_1 = _evidence(runtime, "observer.landscape.first", "viewpoint", phase="first")
    evidence_2 = _evidence(runtime, "observer.landscape.second", "harbor", phase="second")
    evidence_3 = _evidence(runtime, "observer.landscape.third", "station", phase="third")

    projected = LandscapeState.empty()
    project_evidence(evidence_1, projected)
    state_1 = projected.snapshot()
    project_evidence(evidence_2, projected)
    state_2 = projected.snapshot()
    project_evidence(evidence_3, projected)
    state_3 = projected.snapshot()

    assert state_1 == {"place": "viewpoint", "phase": "first", "changed": True}
    assert state_2 == {"place": "harbor", "phase": "second", "changed": True}
    assert state_3 == {"place": "station", "phase": "third", "changed": True}

    assert len(projected.evidence) == 3
    assert projected.evidence == [evidence_1, evidence_2, evidence_3]

    replayed = replay_landscape([evidence_1, evidence_2, evidence_3])
    assert replayed == state_3

    assert evidence_1.transition_data["phase"] == "first"
    assert evidence_2.transition_data["phase"] == "second"
    assert evidence_3.transition_data["phase"] == "third"
