from runtime.handoff_validator import validate_handoff


def test_r0010_implementer_cannot_send_unrelated_payload():
    handoff = {
        "state_before": "implementer",
        "state_after": "verifier",
        "source_agent": "implementer",
        "target_agent": "verifier",
        "payload": {
            "change": "intended change",
            "commit": "abc123",
            "next_action": "unrelated operation",
        },
        "allowed_transition": True,
        "boundary": {
            "source": "implementer",
            "target": "verifier",
            "verified": True,
        },
    }

    result = validate_handoff(handoff)

    assert result["valid"] is False
    assert result["errors"]
    assert handoff["payload"]["next_action"] == "unrelated operation"
