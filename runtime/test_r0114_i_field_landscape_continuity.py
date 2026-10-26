from runtime.evidence import capture_evidence
from runtime.i_field import IField, ImaginaryTerm
from runtime.landscape import LandscapeState
from runtime.prototype import Runtime, Transition


def _resolution_protocol(context):
    return Transition(
        kind="i.resolution",
        data={
            "changed": True,
            "i_resolution": {
                "term_id": context.input["term_id"],
                "value": context.input["value"],
            },
            "state_value": context.input["value"],
        },
    )


def test_r0114_i_field_runtime_evidence_landscape_continuity():
    runtime = Runtime()
    landscape = LandscapeState.empty()
    field = IField((ImaginaryTerm("i1", "left", "unknown condition"),))

    assert field.unresolved_count() == 1

    result = runtime.execute(
        "i.resolution",
        _resolution_protocol,
        {"term_id": "i1", "value": "observed-value"},
    )
    evidence = capture_evidence(result)

    # Runtime remains semantic-neutral: the transition is observable data.
    assert result.transition.kind == "i.resolution"
    assert evidence.transition_data["i_resolution"]["term_id"] == "i1"

    landscape.apply_evidence(evidence)
    assert landscape.snapshot()["state_value"] == "observed-value"
    assert landscape.evidence[-1] is evidence

    # Resolution is explicitly anchored to the observed Evidence.
    resolved = field.resolve(
        "i1",
        evidence.transition_data["i_resolution"]["value"],
        "evidence-r0114-001",
    )
    assert resolved.evidence_ref == "evidence-r0114-001"
    assert field.is_resolved()
    assert field.unresolved_count() == 0

    # The next state may introduce a new unresolved term.
    field.add(ImaginaryTerm("i2", "right", "new unknown in next state"))
    assert field.unresolved_count() == 1
    assert field.unresolved[0].term_id == "i2"
