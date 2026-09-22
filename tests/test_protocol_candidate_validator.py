from runtime.protocol_candidate_validator import validate_protocol_candidate


def valid_candidate() -> dict:
    return {
        "matome": {
            "status": "candidate",
            "authority": False,
            "executable": False,
        },
        "provenance": {
            "candidate_identity": "test-candidate",
            "generator_identity": "test-generator",
            "generation_context": {"intent": "test"},
            "generation_timestamp": "2026-09-22",
            "source_evidence": ["test"],
            "immutable": True,
        },
        "intent": {"statement": "test"},
        "boundary": {"must_not": ["guess"]},
        "context": {"input": ["request"]},
        "behavior": {"if_information_insufficient": ["ask"]},
        "dead_mans_test": {"result": "pass"},
        "quality_checks": {
            "observable_behavior": "pass",
            "required_behavior": "pass",
            "missing_information_check": "pass",
            "question_behavior": "pass",
            "boundary_check": "pass",
            "authority_check": "pass",
        },
        "execution": {
            "approved": False,
            "approval_envelope": None,
            "activation": None,
            "scheduler": None,
            "runner": None,
        },
        "human_gate": {
            "required": True,
            "promotion_target": "Approved Protocol",
            "promotion_authority": "Human",
        },
        "evidence": {"generation_record": True},
        "fail_closed": ["attempted automatic promotion"],
    }


def test_valid_candidate_passes_without_authority():
    result = validate_protocol_candidate(valid_candidate())
    assert result["valid"] is True
    assert result["authority"] is False
    assert result["executable"] is False


def test_approval_or_activation_cannot_be_embedded():
    candidate = valid_candidate()
    candidate["execution"]["approved"] = True
    candidate["execution"]["activation"] = "activate-now"

    result = validate_protocol_candidate(candidate)

    assert result["valid"] is False
    assert any("approved" in error for error in result["errors"])
    assert any("activation" in error for error in result["errors"])


def test_missing_provenance_fails_closed():
    candidate = valid_candidate()
    del candidate["provenance"]["generator_identity"]

    result = validate_protocol_candidate(candidate)

    assert result["valid"] is False
    assert any("provenance" in error for error in result["errors"])


def test_quality_failure_does_not_become_approval():
    candidate = valid_candidate()
    candidate["quality_checks"]["question_behavior"] = "fail"

    result = validate_protocol_candidate(candidate)

    assert result["valid"] is False
    assert result["authority"] is False
