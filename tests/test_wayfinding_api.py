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


def test_wayfinding_api_calls_optional_queue_context_without_changing_vertical_slice():
    result = execute_wayfinding_request(
        {
            "thread": {"thread_id": "natural-language", "posts": [{"participant_id": "p1", "text": "ヒンメルだったらこうした"}]},
            "small_step": {"action": "ask one concrete question"},
            "thread_rpg_queue": {
                "recent_turns": ["ガンダムの比喩", "あしたのジョー", "フリーレン", "ヒンメルだったらこうした", "で？", "研究へ戻る"],
                "semantic_connections": [{"source": "で？", "target": "研究へ戻る", "relation": "research_return"}],
                "imaginary_terms": [{"term_id": "wish", "subject": "user", "text": "愛されたい"}],
                "phase_rotation": {"origin": "今ここ", "centroid": "対話の重心", "model": "3d-phase-rotation-eisenhower"},
            },
        }
    )

    assert result["after"]["changed"] is True
    context = result["thread_rpg_queue"]
    assert context["recent_turns"] == ["あしたのジョー", "フリーレン", "ヒンメルだったらこうした", "で？", "研究へ戻る"]
    assert context["new_semantic_connections"][0]["relation"] == "research_return"
    assert context["unresolved_imaginary_terms"][0]["text"] == "愛されたい"
    assert context["authority"] == "descriptive_only"
