"""Compare the same external model with and without the OPPAI/runtime path.

This is an experiment harness, not Runtime Core. It records both outputs
without treating either output as Domain Semantic Truth.
Requires ANTHROPIC_API_KEY at execution time.
"""

import json
import sys

from examples.adapters.anthropic_adapter import AnthropicAdapter
from runtime.oppai_runtime_flow import execute


PROTOCOL = "shirakami-short-group-scene-v32"


def main() -> None:
    text = sys.stdin.read().strip()
    if not text:
        raise SystemExit("stdin must contain a Landscape/task text")

    adapter = AnthropicAdapter()

    # Same adapter/model and same task text are used for both paths.
    direct_output = adapter(text, {})
    oppai_result = execute(text, adapter, protocol=PROTOCOL)

    print(json.dumps({
        "experiment_id": "short-group-scene-direct-vs-oppai-001",
        "protocol": PROTOCOL,
        "input": text,
        "direct": {
            "model_output": direct_output,
        },
        "oppai": {
            "observation": oppai_result.get("observation"),
            "model_output": oppai_result.get("output"),
            "evidence": oppai_result.get("evidence"),
        },
        "comparison_boundary": {
            "same_model": True,
            "same_input": True,
            "quality_conclusion": "not_claimed",
            "personality_conclusion": "not_claimed",
        },
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
