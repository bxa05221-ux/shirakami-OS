from evidence import capture_evidence
from landscape import LandscapeState
from prototype import Transition, execute_protocol


def test_observable_transition_survives_event_state_evidence_landscape_boundary():
    protocol = {
        "matome": {
            "title": "Boundary Preservation Test",
            "version": "0.1",
        }
    }

    def transition(value):
        return Transition(
            kind="boundary.observation",
            data={
                "changed": True,
                "observation": value,
                "symbolic_reference": "local.story",
            },
        )

    execution = execute_protocol(
        protocol,
        transition,
        input_value={"place": "shore", "note": "unexpected detail"},
    )
    assert execution.result.status == "completed"

    evidence = capture_evidence(execution.result)
    landscape = LandscapeState.empty()
    landscape.apply_evidence(evidence)

    assert landscape.snapshot() == {
        "changed": True,
        "observation": {
            "place": "shore",
            "note": "unexpected detail",
        },
        "symbolic_reference": "local.story",
    }
    assert dict(evidence.transition_data) == landscape.snapshot()
