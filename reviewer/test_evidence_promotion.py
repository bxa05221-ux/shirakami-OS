from reviewer.evidence_promotion import (
    EvidencePromotionRequest,
    candidate_evidence_ids,
    promote_review_evidence,
)
from runtime.evidence import EvidenceRecord
from runtime.evidence_store import EvidenceStore


def store_with_record():
    record = EvidenceRecord(
        protocol_id="P1",
        status="completed",
        transition_kind="test:observed",
        transition_data={"changed": True},
        signals=("observed",),
    )
    return EvidenceStore().append(record), record


def test_reviewer_ids_are_candidates_until_human_gate():
    store, record = store_with_record()
    request = EvidencePromotionRequest(
        reviewer_id="reviewer-a",
        evidence_ids=(record.evidence_id,),
    )
    try:
        promote_review_evidence(store, request)
    except ValueError as exc:
        assert "Human Gate" in str(exc)
    else:
        raise AssertionError("pending review must not promote Evidence")


def test_human_gate_approval_returns_existing_immutable_records():
    store, record = store_with_record()
    request = EvidencePromotionRequest(
        reviewer_id="reviewer-a",
        evidence_ids=(record.evidence_id,),
        human_decision="approved",
    )
    accepted = promote_review_evidence(store, request)
    assert accepted == (record,)
    assert accepted[0].evidence_id == record.evidence_id
    assert store.all() == (record,)


def test_unknown_reviewer_reference_is_rejected_even_after_approval():
    store, _ = store_with_record()
    request = EvidencePromotionRequest(
        reviewer_id="reviewer-a",
        evidence_ids=("does-not-exist",),
        human_decision="approved",
    )
    try:
        promote_review_evidence(store, request)
    except ValueError as exc:
        assert "unknown Evidence IDs" in str(exc)
    else:
        raise AssertionError("unknown Evidence must not be accepted")


def test_candidate_normalization_does_not_accept_evidence():
    assert candidate_evidence_ids(["E1", "", "E1", "E2"]) == ("E1", "E2")
