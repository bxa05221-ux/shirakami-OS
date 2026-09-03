from runtime.evidence import EvidenceRecord
from runtime.prototype import ExecutionResult, Transition


def test_r0010_evidence_record_preserves_captured_data():
    result = ExecutionResult(
        status="failed",
        protocol_id="r0010",
        transition=Transition(
            kind="VERIFY",
            data={"changed": False, "result": "failed"},
        ),
        signals=("verification_failed",),
    )
    evidence = EvidenceRecord.from_result(result)

    original_data = dict(evidence.transition_data)

    try:
        evidence.transition_data["result"] = "passed"
    except TypeError:
        pass

    assert dict(evidence.transition_data) == original_data
    assert evidence.signals == ("verification_failed",)
