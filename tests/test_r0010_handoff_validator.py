from runtime.r0010_handoff_validator import validate_handoff


def valid_handoff():
    return {
        "state_before": "OBSERVE",
        "state_after": "AUDIT",
        "source_agent": "observer",
        "target_agent": "auditor",
        "payload": {
            "current_state": "observed",
            "detected_gap": "none",
        },
        "allowed_transition": True,
        "boundary": {
            "source": "observer",
            "target": "auditor",
            "verified": True,
        },
    }


def test_valid_observer_to_auditor_handoff():
    result = validate_handoff(valid_handoff())
    assert result["valid"] is True


def test_invalid_direct_observer_to_verifier_is_rejected():
    handoff = valid_handoff()
    handoff["target_agent"] = "verifier"
    handoff["state_after"] = "VERIFY"
    handoff["boundary"]["target"] = "verifier"
    result = validate_handoff(handoff)
    assert result["valid"] is False


def test_payload_crossing_source_boundary_is_rejected():
    handoff = valid_handoff()
    handoff["payload"]["commit"] = "unrelated-change"
    result = validate_handoff(handoff)
    assert result["valid"] is False


def test_invalid_allowed_transition_is_rejected_without_repair():
    handoff = valid_handoff()
    handoff["allowed_transition"] = False
    result = validate_handoff(handoff)
    assert result["valid"] is False
    assert handoff["allowed_transition"] is False
