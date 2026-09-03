from runtime.evidence import EvidenceRecord


def test_r0010_evidence_record_preserves_captured_data():
    evidence = EvidenceRecord(
        protocol_id="r0010",
        status="failed",
        transition_kind="VERIFY",
        transition_data={"changed": False, "result": "failed"},
        signals=("verification_failed",),
    )

    original_data = dict(evidence.transition_data)

    try:
        evidence.transition_data["result"] = "passed"
    except TypeError:
        pass

    assert dict(evidence.transition_data) == original_data
    assert evidence.signals == ("verification_failed",)
