from runtime.handoff_validator import validate_handoff


TRANSITIONS = [
    ("observer", "auditor", {"facts": "observed", "current_state": "OBSERVE", "detected_gap": "test"}),
    ("auditor", "implementer", {"confirmed_boundary": "test", "risk": "low", "minimal_change_candidate": "test"}),
    ("implementer", "verifier", {"change": "test", "commit": "test"}),
    ("verifier", "confirmer", {"pass": True, "fail": False, "evidence": "test"}),
]


def test_r0010_normal_path_accepts_each_declared_transition():
    for source, target, payload in TRANSITIONS:
        result = validate_handoff(
            {
                "state_before": source,
                "state_after": target,
                "source_agent": source,
                "target_agent": target,
                "payload": payload,
                "allowed_transition": True,
                "boundary": {
                    "source": source,
                    "target": target,
                    "verified": True,
                },
            }
        )

        assert result["valid"] is True
