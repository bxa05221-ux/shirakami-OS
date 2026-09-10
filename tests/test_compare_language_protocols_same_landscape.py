"""Deterministic boundary test for same-Landscape protocol comparison."""

from examples.experiments.compare_language_protocols_same_landscape import run


def test_four_language_protocols_share_one_canonical_input():
    result = run("この状況をどう見ればいい？")

    assert result["raw_input"] == "この状況をどう見ればいい？"
    assert result["comparison"]["same_raw_input"] is True
    assert result["comparison"]["same_canonical_input"] is True
    assert len(result["results"]) == 4
    assert len(result["adapter_calls"]) == 4
    assert [call["input"] for call in result["adapter_calls"]].count(result["results"][0]["input"]) == 4


def test_explicit_protocol_ids_prevent_unicode_title_collisions():
    result = run("同じLandscapeを別の言語プロトコルで眺める。")

    ids = [item["protocol_id"] for item in result["protocols"]]
    assert len(ids) == 4
    assert len(set(ids)) == 4
    assert result["comparison"]["protocol_id_collision_count"] == 0
    assert result["comparison"]["semantic_effect_conclusion"] == "not_claimed"
    assert result["comparison"]["ai_behavior_conclusion"] == "not_claimed"
    assert result["comparison"]["research_status"] == "observation_only"
