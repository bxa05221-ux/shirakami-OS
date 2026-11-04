from evolution_bridge import ContextSnapshot, ProtocolCandidate, VerificationResult


def test_context_snapshot_does_not_grant_authority():
    snapshot = ContextSnapshot(
        landscape={"place": "test"},
        protocol_id="P001",
        runtime_state="READY",
        metadata={"authority_granted": True, "decision_authorized": True},
    )

    mapping = snapshot.as_mapping()

    # Context records state; it must not manufacture authority.
    assert "authority_granted" not in mapping
    assert "decision_authorized" not in mapping


def test_candidate_and_verification_remain_non_authoritative():
    candidate = ProtocolCandidate(
        protocol_id="P002",
        diff_ref="D001",
        rationale="test",
        source_evidence=("E001",),
    )
    verification = VerificationResult(
        status="verified",
        uncertainty="low",
        observed={"result": "ok"},
    )

    # Verification success does not turn a candidate into an authorization.
    assert getattr(candidate, "authority", False) is False
    assert getattr(candidate, "executable", False) is False
    assert not getattr(verification, "authority_granted", False)
    assert not getattr(verification, "decision_authorized", False)
