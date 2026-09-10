import json
import sys
from unittest.mock import patch

from examples.experiments.compare_short_group_scene_direct_vs_oppai import main


def test_comparison_harness_keeps_direct_and_oppai_outputs_distinct(capsys):
    calls = []

    class FakeAdapter:
        def __call__(self, input_text, context):
            calls.append((input_text, context))
            return f"fake-output-{len(calls)}"

    # The harness constructs its adapter internally, so replace the class at
    # module boundary. No external API is contacted by this test.
    with patch(
        "examples.experiments.compare_short_group_scene_direct_vs_oppai.AnthropicAdapter",
        return_value=FakeAdapter(),
    ):
        with patch.object(sys, "stdin") as stdin:
            stdin.read.return_value = "same landscape"
            main()

    payload = json.loads(capsys.readouterr().out)
    assert payload["input"] == "same landscape"
    assert payload["direct"]["model_output"] == "fake-output-1"
    assert payload["oppai"]["model_output"] == "fake-output-2"
    assert payload["comparison_boundary"]["same_model"] is True
    assert payload["comparison_boundary"]["same_input"] is True
    assert payload["comparison_boundary"]["quality_conclusion"] == "not_claimed"
    assert len(calls) == 2
