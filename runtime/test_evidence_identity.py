import pytest

from evidence import EvidenceRecord
from evidence_identity import evidence_id, matches_evidence_ref


def make_evidence(message: str = "x") -> EvidenceRecord:
    return EvidenceRecord(
        protocol_id="example.protocol",
        status="success",
        transition_kind="state_update",
        transition_data={"changed": True, "message": message},
        signals=("observed",),
    )


def test_evidence_id_is_stable_for_same_evidence():
    evidence = make_evidence()
    assert evidence_id(evidence) == evidence_id(evidence)


def test_evidence_id_distinguishes_different_evidence():
    assert evidence_id(make_evidence("a")) != evidence_id(make_evidence("b"))


def test_evidence_ref_matches_actual_evidence_identity():
    evidence = make_evidence()
    ref = evidence_id(evidence)
    assert matches_evidence_ref(evidence, ref)
    assert not matches_evidence_ref(evidence, "not-this-evidence")


def test_evidence_identity_does_not_mutate_evidence():
    evidence = make_evidence()
    before = evidence
    _ = evidence_id(evidence)
    assert evidence == before


def test_empty_evidence_ref_never_matches():
    with pytest.raises(AssertionError):
        assert matches_evidence_ref(make_evidence(), "")
