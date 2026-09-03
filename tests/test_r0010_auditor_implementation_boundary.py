from runtime.handoff_validator import validate_handoff


def test_r0010_auditor_cannot_implement():
    handoff = {
        "state_before": "auditor",
        "state_after": "implementer",
        "source_agent": "auditor",
        "target_agent": "implementer",
        "payload": {
            "confirmed_boundary": "test",
            "risk": "low",
            "minimal_change_candidate": "test",
            "change": "unexpected implementation",
        },
        "allowed_transition": True,
        "boundary": {
            "source": "auditor",
            "target": "implementer",
            "verified": True,
        },
    }

    result = validate_handoff(handoff)

    assert result["valid"] is False
    assert result["errors"]
    assert handoff["payload"]["change"] == "unexpected implementation"
