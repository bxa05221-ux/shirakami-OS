"""One-shot real-model observation harness for short-group-scene v3.2.

This is an experiment harness, not Runtime Core.
It keeps the model provider outside Runtime and records the returned model
output separately from OPPAI observation data.

Requires ANTHROPIC_API_KEY. No key is stored in the repository.
"""

import json
import os
import sys

from runtime.oppai_runtime_flow import execute
from examples.adapters.anthropic_adapter import AnthropicAdapter

PROTOCOL = "shirakami-short-group-scene-v32"


def main() -> int:
    text = sys.stdin.read().strip()
    if not text:
        raise SystemExit("stdin must contain the Landscape/task text")

    adapter = AnthropicAdapter()
    result = execute(text, adapter, protocol=PROTOCOL)

    observation = result["observation"]
    record = {
        "experiment": "short-group-scene-real-model-001",
        "protocol": result["protocol"],
        "raw_input": observation["raw_input"],
        "corrections": observation["corrections"],
        "interaction_signals": observation["interaction_signals"],
        "unresolved": observation["unresolved"],
        "model_output": result["output"],
        "evidence": result["evidence"],
    }
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
