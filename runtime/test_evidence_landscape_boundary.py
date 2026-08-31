from runtime.landscape import LandscapeState
from runtime.evidence import capture_evidence
from runtime.prototype import Transition


def test_evidence_can_cross_into_landscape_without_runtime_owning_meaning():
    transition = Transition(
        kind="symbolic.reference",
        data={
            "reference": "grandfather.said",
            "changed": True,
        },
    )

    evidence = capture_evidence(transition)
    landscape = LandscapeState.empty()
    landscape.apply_evidence(evidence)

    assert evidence.transition.kind == "symbolic.reference"
    assert evidence.transition.data["reference"] == "grandfather.said"
    assert landscape.evidence[-1] == evidence
    assert landscape.evidence[-1].transition.data["reference"] == "grandfather.said"

    # The boundary preserves the observable transition; it does not require
    # LandscapeState or Runtime to interpret what the symbolic reference means.
    assert not hasattr(landscape, "symbolic_meaning")
