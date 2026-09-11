from runtime.evidence import capture_evidence
from runtime.i_field import IField, ImaginaryTerm
from runtime.prototype import Runtime, Transition


def _resolution_protocol(context):
    return Transition(
        kind=f"i.resolution.{context.input['side']}",
        data={
            "changed": True,
            "i_resolution": {
                "term_id": context.input["term_id"],
                "value": context.input["value"],
            },
        },
    )


def test_i_lifecycle_runtime_evidence_resolution_and_next_state():
    runtime = Runtime()
    field = IField(
        (
            ImaginaryTerm("i_left", "left", "unknown left-side condition"),
            ImaginaryTerm("i_right", "right", "unknown right-side condition"),
        )
    )

    result_left = runtime.execute(
        "i.resolution.left",
        _resolution_protocol,
        {"term_id": "i_left", "side": "left", "value": "left-evidence"},
    )
    evidence_left = capture_evidence(result_left)
    field.resolve(
        "i_left",
        evidence_left.transition_data["i_resolution"]["value"],
        "evidence-left-001",
    )

    assert field.unresolved_count() == 1
    assert field.unresolved[0].term_id == "i_right"
    assert evidence_left.transition_data["i_resolution"]["term_id"] == "i_left"

    result_right = runtime.execute(
        "i.resolution.right",
        _resolution_protocol,
        {"term_id": "i_right", "side": "right", "value": "right-evidence"},
    )
    evidence_right = capture_evidence(result_right)
    field.resolve(
        "i_right",
        evidence_right.transition_data["i_resolution"]["value"],
        "evidence-right-001",
    )

    assert field.is_resolved()
    assert {item.term_id for item in field.resolved} == {"i_left", "i_right"}
    assert {item.side for item in field.resolved} == {"left", "right"}

    # The next state may introduce a new unresolved term.
    field.add(ImaginaryTerm("i_next", "right", "new unknown in the next state"))
    assert field.unresolved_count() == 1
    assert field.unresolved[0].term_id == "i_next"
