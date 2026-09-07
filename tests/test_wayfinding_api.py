from runtime.wayfinding_api import execute_wayfinding_request


def test_wayfinding_api_executes_complete_cycle():
    result = execute_wayfinding_request(
        {
            "thread": {
                "thread_id": "t1",
                "participants": [{"participant_id": "p1", "persona": {"style": "quiet"}}],
                "posts": [{"participant_id": "p1", "text": "まず入口を確認しよう", "aa": "(｀・ω・´)"}],
            },
            "landscape": {"location": "start"},
            "small_step": {"action": "inspect", "reason": "reduce uncertainty"},
            "transition": {"kind": "wayfinding.small_step", "data": {"location": "checkpoint"}},
        }
    )
    assert result["narrative"] == "まず入口を確認しよう"
    assert result["viewpoints"][0]["aa"] == "(｀・ω・´)"
    assert result["before"] == {"location": "start"}
    assert result["small_step"]["action"] == "inspect"
    assert result["evidence"]["transition_kind"] == "wayfinding.small_step"
    assert result["after"]["location"] == "checkpoint"


def test_wayfinding_api_preserves_opaque_persona():
    result = execute_wayfinding_request(
        {
            "thread": {
                "thread_id": "t2",
                "participants": [{"participant_id": "p1", "persona": {"ip": "later-extension"}}],
                "posts": [{"participant_id": "p1", "text": "ok"}],
            },
            "small_step": {"action": "wait"},
        }
    )
    assert result["viewpoints"][0]["participant_id"] == "p1"
