from runtime.oppai_runtime_flow import execute


PROTOCOL = "shirakami-short-group-scene-v32"


def test_short_group_scene_reaches_replaceable_adapter():
    calls = []

    def adapter(canonical_prompt, protocol):
        calls.append((canonical_prompt, protocol))
        return {
            "observation": "same landscape",
            "response": "first voice",
            "reaction": "second voice",
            "correction_or_alignment": "small adjustment",
            "unresolved_or_temporary_landing": True,
        }

    result = execute(
        "同じLandscapeを、短い群像劇として見てみる",
        adapter,
        protocol=PROTOCOL,
    )

    assert calls
    assert calls[0][1] == PROTOCOL
    assert calls[0][0] == result["input"]
    assert result["protocol"] == PROTOCOL
    assert result["output"]["reaction"] == "second voice"
    assert result["output"]["unresolved_or_temporary_landing"] is True
    assert result["evidence"]["raw_preserved"] is True
