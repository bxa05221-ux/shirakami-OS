from runtime.handoff_validator import validate_handoff


def test_r0010_verifier_cannot_auto_fix():
    handoff = {
        "state_before": "verifier",
        "state_after": "confirmer",
        "source_agent": "verifier",
        "target_agent": "confirmer",
        "payload": {
            "pass": False,
            "fail": True,
            "evidence": "verification failed",
            "fix": "apply automatic repair",
        },
        "allowed_transition": True,
        "boundary": {
            "source": "verifier",
            "target": "confirmer",
            "verified": True,
        },
    }

    result = validate_handoff(handoff)

    assert result["valid"] is False
    assert any("payload keys" in error for error in result["errors"])
    assert handoff["payload"]["fix"] == "apply automatic repair"
