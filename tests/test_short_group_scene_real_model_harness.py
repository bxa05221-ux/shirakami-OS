import io
import json
import sys

from examples.experiments import run_short_group_scene_real_model as harness


class FakeAdapter:
    def __call__(self, input_text, protocol):
        assert protocol == "shirakami-short-group-scene-v32"
        return {
            "observation": "fake-model-observation",
            "protocol": protocol,
            "input": input_text,
            "output": "fake model output",
        }


def test_real_model_harness_keeps_adapter_output_separate(monkeypatch, capsys):
    monkeypatch.setattr(harness, "AnthropicAdapter", lambda: FakeAdapter())
    monkeypatch.setattr(
        sys,
        "stdin",
        io.StringIO("A landscape/task for the experiment"),
    )

    assert harness.main() == 0

    record = json.loads(capsys.readouterr().out)
    assert record["experiment"] == "short-group-scene-real-model-001"
    assert record["protocol"] == "shirakami-short-group-scene-v32"
    assert record["raw_input"] == "A landscape/task for the experiment"
    assert record["model_output"] == "fake model output"
    assert record["evidence"] is not None
