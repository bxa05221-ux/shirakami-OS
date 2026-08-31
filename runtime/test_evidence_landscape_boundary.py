from runtime.landscape import LandscapeState
from runtime.evidence import capture_evidence
from runtime.prototype import Transition, execute_protocol


def test_evidence_can_cross_into_landscape_without_runtime_owning_meaning():
    protocol = {
        "matome": {
            "title": "Evidence Landscape Boundary Test",
            "version": "0.1",
        }
    }

    def transition(value):
        return Transition(
            kind="symbolic.reference",
            data={
                "reference": "grandfather.said",
                "changed": True,
                "input": value,
            },
        )

    execution = execute_protocol(
        protocol,
        transition,
        input_value={"context": "current-situation"},
    )
    assert execution.result.status == "completed"

    evidence = capture_evidence(execution.result)
    landscape = LandscapeState.empty()
    landscape.apply_evidence(evidence)

    assert evidence.transition_kind == "symbolic.reference"
    assert evidence.transition_data["reference"] == "grandfather.said"
    assert landscape.evidence[-1] == evidence
    assert landscape.evidence[-1].transition_data["reference"] == "grandfather.said"

    # The boundary preserves the observable transition; it does not require
    # LandscapeState or Runtime to interpret what the symbolic reference means.
    assert not hasattr(landscape, "symbolic_meaning")
