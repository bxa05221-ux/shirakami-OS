from runtime.human_gate import HumanGateDecision
from runtime.structural_validation_human_gate import (
    process_validated_candidate,
    to_human_gate_input,
)


def valid_result():
    return {
        "valid": True,
        "errors": (),
        "candidate_identity": "candidate-001",
        "origin_observation_identity": "observation-001",
        "protocol_identity": "protocol-001",
        "provenance": ("observation-001",),
        "evidence_ids": ("evidence-001",),
        "authority": False,
        "executable": False,
    }


def test_explicit_metadata_maps_without_creating_authority():
    candidate = to_human_gate_input(valid_result())
    assert candidate["candidate_identity"] == "candidate-001"
    assert candidate["protocol_identity"] == "protocol-001"
    assert candidate["provenance"] == ("observation-001",)
    assert candidate["evidence_ids"] == ("evidence-001",)
    assert candidate["validation"] is True
    assert candidate["authority"] is False
    assert candidate["executable"] is False


def test_validation_pass_does_not_approve():
    result = process_validated_candidate(
        validation_result=valid_result(),
        reviewer_identity="reviewer-001",
        decision="reject",
    )
    assert isinstance(result, HumanGateDecision)
    assert result.decision == "reject"
    assert result.approval_envelope is None


def test_explicit_human_approval_preserves_metadata():
    result = process_validated_candidate(
        validation_result=valid_result(),
        reviewer_identity="reviewer-001",
        decision="approve",
    )
    assert result.decision == "approve"
    assert result.approval_envelope is not None
    assert result.approval_envelope.protocol_id == "protocol-001"
    assert result.approval_envelope.provenance == ("observation-001",)
    assert result.approval_envelope.evidence_ids == ("evidence-001",)


def test_missing_approval_metadata_fails_closed():
    missing = valid_result()
    del missing["protocol_identity"]

    try:
        to_human_gate_input(missing)
    except ValueError as exc:
        assert "missing explicit approval metadata" in str(exc)
    else:
        raise AssertionError("missing approval metadata must fail closed")


def test_candidate_identity_is_not_used_as_protocol_identity():
    missing = valid_result()
    del missing["protocol_identity"]

    try:
        to_human_gate_input(missing)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "candidate identity must not be inferred as protocol identity"
        )


def test_invalid_validation_cannot_reach_human_gate():
    invalid = valid_result()
    invalid["valid"] = False

    try:
        to_human_gate_input(invalid)
    except ValueError as exc:
        assert "validation result must be PASS" in str(exc)
    else:
        raise AssertionError("invalid validation must fail closed")


def test_missing_reviewer_is_not_inferred():
    candidate = to_human_gate_input(valid_result())

    try:
        process_validated_candidate(
            validation_result=valid_result(),
            reviewer_identity="",
            decision="approve",
        )
    except ValueError as exc:
        assert "missing reviewer identity" in str(exc)
    else:
        raise AssertionError("missing reviewer must fail closed")

    assert candidate["authority"] is False
