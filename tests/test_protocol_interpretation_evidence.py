"""Characterization of misinterpretation records, not semantic AI grading."""
from dataclasses import FrozenInstanceError
import pytest

from runtime.protocol_interpretation_evidence import (
    InterpretationEvidence, InterpretationEvidenceError, review_interpretation,
)


def sample(**changes):
    args = dict(
        evidence_id="thread-rpg-case-001",
        protocol_ref="protocols/thread-rpg-v1.2.1.yaml",
        protocol_revision="1.2.1",
        input_ref="sample-input-001",
        original_output="1: イッチ\n2: 名無しA >>1 いや違うだろ\n3: 名無しB >>2 ｗ",
        observed_output="1: 技術派は賛成\n2: 慎重派は反対\nまとめ: 両方大事",
        claimed_difference="Anonymous participants only enumerate views and force a summary",
        category="forced_conclusion",
        observer="test-observer",
    )
    args.update(changes)
    return InterpretationEvidence(**args)


def test_candidate_preserves_both_outputs_and_source_lineage():
    candidate = sample()
    record = candidate.as_record()
    assert record["status"] == "candidate_only"
    assert record["original_output"].startswith("1: イッチ")
    assert "まとめ:" in record["observed_output"]
    assert record["protocol_ref"] == "protocols/thread-rpg-v1.2.1.yaml"
    assert record["input_ref"] == "sample-input-001"
    assert record["runtime_evidence"] is False
    assert record["authorizes_execution"] is False
    assert record["changes_canonical_protocol"] is False


@pytest.mark.parametrize("field,value", [
    ("protocol_ref", ""), ("protocol_revision", ""),
    ("input_ref", ""), ("original_output", ""),
    ("observed_output", ""), ("claimed_difference", ""),
    ("observer", ""), ("category", "invented_claim"),
])
def test_missing_or_unknown_provenance_fails_closed(field, value):
    with pytest.raises(InterpretationEvidenceError):
        sample(**{field: value})


def test_review_preserves_original_candidate_without_protocol_promotion():
    original = sample()
    reviewed = review_interpretation(
        original, reviewer="human", review_note="Output appears to force closure",
        accepted_as_observation=True,
    )
    assert original.status == "candidate_only"
    assert reviewed.status == "reviewed"
    assert reviewed.original_output == original.original_output
    assert reviewed.observed_output == original.observed_output
    assert reviewed.as_record()["authorizes_execution"] is False
    assert reviewed.as_record()["changes_canonical_protocol"] is False
    with pytest.raises(InterpretationEvidenceError):
        review_interpretation(reviewed, reviewer="human", review_note="again",
                              accepted_as_observation=True)


def test_reviewer_can_reject_candidate_without_erasing_data():
    original = sample(category="isolated_perspectives")
    reviewed = review_interpretation(
        original, reviewer="human", review_note="Contradiction not established",
        accepted_as_observation=False,
    )
    assert reviewed.status == "rejected"
    assert reviewed.observed_output == original.observed_output


def test_candidate_cannot_self_certify_or_change_its_fields():
    with pytest.raises(InterpretationEvidenceError):
        sample(status="reviewed")
    with pytest.raises(InterpretationEvidenceError):
        sample(status="candidate_only", reviewer="AI", review_note="definitely wrong")
    with pytest.raises(FrozenInstanceError):
        sample().status = "reviewed"


def test_review_requires_explicit_human_rationale():
    with pytest.raises(InterpretationEvidenceError):
        review_interpretation(sample(), reviewer="", review_note="reason",
                              accepted_as_observation=True)
    with pytest.raises(InterpretationEvidenceError):
        review_interpretation(sample(), reviewer="human", review_note="",
                              accepted_as_observation=True)
