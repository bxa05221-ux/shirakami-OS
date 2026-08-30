from runtime.oppai_runtime_flow import execute, prepare


def test_prepare_keeps_human_operation_natural():
    result = prepare("いや、そこじゃない。普通に話していいんだ。")

    assert result.input_for_runtime == result.observation.canonical_prompt
    assert result.observation.raw_input == "いや、そこじゃない。普通に話していいんだ。"
    assert result.evidence["raw_preserved"] is True
    assert result.evidence["corrections_preserved"] is True


def test_execute_uses_replaceable_runtime_adapter():
    calls = []

    def adapter(value, protocol):
        calls.append((value, protocol))
        return "runtime-result"

    result = execute("これ、どうなる？", adapter, protocol="thread-rpg")

    assert result["output"] == "runtime-result"
    assert calls == [("これ、どうなる？", "thread-rpg")]
    assert result["observation"]["unresolved"] == ["これ、どうなる？"]
