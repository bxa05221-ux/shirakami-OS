from runtime.approval_envelope_provenance import enrich_human_gate_input


def base_result():
    return {
        "valid": True,
        "candidate_identity": "candidate-001",
        "authority": False,
        "executable": False,
    }


def test_missing_approval_metadata_fails_closed():
    try:
        enrich_human_gate_input(base_result())
    except ValueError as exc:
        assert "missing explicit approval metadata" in str(exc)
    else:
        raise AssertionError("missing approval metadata must fail closed")


def test_explicit_metadata_is_preserved_without_inference():
    result = base_result()
    result.update(
        {
            "protocol_identity": "protocol-001",
            "provenance": ("observation-001",),
            "evidence_ids": ("evidence-001",),
        }
    )
    mapped = enrich_human_gate_input(result)
    assert mapped["candidate_identity"] == "candidate-001"
    assert mapped["protocol_identity"] == "protocol-001"
    assert mapped["provenance"] == ("observation-001",)
    assert mapped["evidence_ids"] == ("evidence-001",)
    assert mapped["authority"] is False
    assert mapped["executable"] is False


def test_candidate_identity_is_not_used_as_protocol_identity():
    result = base_result()
    result.update(
        {
            "provenance": ("observation-001",),
            "evidence_ids": (),
        }
    )
    try:
        enrich_human_gate_input(result)
    except ValueError as exc:
        assert "protocol_identity" in str(exc)
    else:
        raise AssertionError("protocol identity must be explicit")
