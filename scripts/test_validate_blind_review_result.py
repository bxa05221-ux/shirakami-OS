from scripts.validate_blind_review_result import validate_blind_review_result


def valid_result():
    return {
        "reviewer_id": "reviewer-alpha",
        "matome_yaml": "matome:\n  reviewer_id: reviewer-alpha\n",
        "objective": "independent observation",
        "observations": ["fact"],
        "evidence_ids": ["E1"],
        "resolved_questions": [],
        "unresolved_questions": ["Q1"],
        "falsifiable_points": ["F1"],
        "proposals": ["P1"],
        "interpretation": ["I1"],
        "human_gate": {"required": True, "decision": "pending"},
    }


def test_valid_blind_review_result_preserves_non_authoritative_boundary():
    result = validate_blind_review_result(valid_result())
    assert result["human_gate"] == {"required": True, "decision": "pending"}


def test_rejects_missing_field():
    result = valid_result()
    result.pop("observations")
    try:
        validate_blind_review_result(result)
    except ValueError as exc:
        assert "observations" in str(exc)
    else:
        raise AssertionError("missing observations must be rejected")


def test_rejects_human_gate_removal():
    result = valid_result()
    result["human_gate"]["required"] = False
    try:
        validate_blind_review_result(result)
    except ValueError as exc:
        assert "human_gate.required" in str(exc)
    else:
        raise AssertionError("Human Gate removal must be rejected")


def test_rejects_decision():
    result = valid_result()
    result["human_gate"]["decision"] = "approved"
    try:
        validate_blind_review_result(result)
    except ValueError as exc:
        assert "decision" in str(exc)
    else:
        raise AssertionError("review result must not create a decision")


def test_rejects_missing_matome_yaml():
    result = valid_result()
    result.pop("matome_yaml")
    try:
        validate_blind_review_result(result)
    except ValueError as exc:
        assert "matome_yaml" in str(exc)
    else:
        raise AssertionError("missing matome_yaml must be rejected")
