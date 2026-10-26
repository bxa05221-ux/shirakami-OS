from evidence import capture_evidence
from landscape import LandscapeState
from prototype import Runtime, Transition


def test_one_evidence_can_propagate_to_multiple_landscapes():
    runtime = Runtime()

    def protocol(context):
        return Transition(
            kind="landscape.transition",
            data={
                "changed": True,
                "source": context.input["source"],
                "value": context.input["value"],
            },
        )

    result = runtime.execute(
        "evidence.propagation",
        protocol,
        {"source": "human", "value": "river"},
    )
    evidence = capture_evidence(result)

    first = LandscapeState.empty()
    second = LandscapeState.empty()

    first.apply_evidence(evidence)
    second.apply_evidence(evidence)

    assert first.snapshot() == second.snapshot()
    assert evidence.transition_data["value"] == "river"


def test_evidence_is_not_mutated_by_landscape_projection():
    runtime = Runtime()

    def protocol(context):
        return Transition(
            kind="landscape.transition",
            data={"changed": True, "value": context.input["value"]},
        )

    result = runtime.execute(
        "evidence.immutable",
        protocol,
        {"value": "water"},
    )
    evidence = capture_evidence(result)
    before = dict(evidence.transition_data)

    landscape = LandscapeState.empty()
    landscape.apply_evidence(evidence)

    assert dict(evidence.transition_data) == before
    assert landscape.snapshot()["value"] == "water"


def test_non_transition_evidence_does_not_propagate():
    runtime = Runtime()

    def protocol(context):
        return Transition(
            kind="observation.only",
            data={"changed": False, "value": context.input["value"]},
        )

    result = runtime.execute(
        "evidence.non_transition",
        protocol,
        {"value": "steam"},
    )
    evidence = capture_evidence(result)

    landscape = LandscapeState.empty()
    landscape.apply_evidence(evidence)

    assert landscape.snapshot() == {}
