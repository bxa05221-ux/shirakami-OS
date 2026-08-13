from evidence import capture_evidence
from prototype import Runtime, example_protocol
from reverse_landscape_flow import (
    derive_delta,
    evidence_id,
    pose_dark_question,
    record_counter_evidence,
    record_reobservation,
    represent_delta,
)


def test_reverse_flow_preserves_evidence_and_creates_new_lineage():
    result = Runtime().execute(
        "example.protocol",
        example_protocol,
        {"message": "reverse flow"},
    )
    evidence = capture_evidence(result)
    original_status = evidence.status
    original_data = dict(evidence.transition_data)

    delta = derive_delta(
        {"message": "before", "changed": False},
        {"message": "after", "changed": True},
        evidence_id(evidence),
    )
    matome = represent_delta(delta, format="yaml")
    question = pose_dark_question(
        matome,
        "この変化を生じさせた別の説明はあるか？",
    )
    counter = record_counter_evidence(
        question,
        {"alternative": "different-cause", "observed": True},
    )
    reobservation = record_reobservation(
        evidence_id(evidence),
        counter,
        "new observation recorded",
    )

    assert delta.changed["message"] == "after"
    assert delta.changed["changed"] is True
    assert matome.format == "yaml"
    assert question.matome is matome
    assert counter.question is question
    assert reobservation.prior_evidence_id == evidence_id(evidence)

    assert evidence.status == original_status
    assert dict(evidence.transition_data) == original_data


def test_delta_does_not_invent_missing_interpretation():
    delta = derive_delta(
        {"focus": "drawing"},
        {"focus": "drawing", "confidence": "high"},
        "root:observation",
    )

    assert dict(delta.changed) == {"confidence": "high"}
    assert "meaning" not in delta.changed
    assert "cause" not in delta.changed
