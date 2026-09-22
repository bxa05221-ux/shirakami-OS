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
        "authority": False,
        "executable": False,
    }


def test_valid_result_maps_without_creating_authority():
    candidate = to_human_gate_input(valid_result())
    assert candidate["candidate_identity"] == "candidate-001"
    assert candidate["provenance"] == ("observation-001",)
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


def test_explicit_human_approval_creates_envelope():
    result = process_validated_candidate(
        validation_result=valid_result(),
        reviewer_identity="reviewer-001",
        decision="approve",
    )
    assert result.decision == "approve"
    assert result.approval_envelope is not None


def test_invalid_validation_cannot_reach_human_gate():
    invalid = dict(valid_result())
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
