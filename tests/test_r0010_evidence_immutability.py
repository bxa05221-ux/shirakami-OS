from runtime.evidence import EvidenceRecord


def test_r0010_evidence_record_preserves_captured_data():
    evidence = EvidenceRecord(
        protocol_id="r0010",
        transition="VERIFY",
        payload={"result": "failed"},
    )

    original = evidence.to_dict()

    try:
        evidence.payload["result"] = "passed"
    except (TypeError, AttributeError):
        pass

    assert evidence.to_dict() == original
