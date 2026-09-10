from examples.experiments.cognitive_echolocalization_loop_001 import run


def test_cognitive_echo_loop_preserves_two_observation_boundaries() -> None:
    result = run("今日はなんだか変だ")

    assert result["experiment"] == "cognitive-echolocalization-loop-001"
    assert result["protocol"] == "shirakami-short-group-scene-v32"
    assert result["loop"]["turns"] == 2
    assert result["loop"]["projection"] == "今日はなんだか変だ"
    assert result["loop"]["echo"].startswith("echo-1:")
    assert result["loop"]["echo_2"].startswith("echo-2:")

    assert len(result["observations"]) == 2
    assert result["observations"][0]["raw_input"] == "今日はなんだか変だ"
    assert "前の反応を受けて再投射:" in result["observations"][1]["raw_input"]

    assert len(result["evidence"]) == 2
    assert all(item["raw_preserved"] is True for item in result["evidence"])
    assert result["interpretation"] == "not_claimed"
    assert result["cognitive_echolocalization_semantics"] == "research_only"

    assert len(result["adapter_calls"]) == 2
    assert all(call["protocol"] == result["protocol"] for call in result["adapter_calls"])
