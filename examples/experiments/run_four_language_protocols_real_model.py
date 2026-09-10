"""Operator-side real-model runner for four language protocols.

This harness keeps provider execution outside Runtime Core. It requires
ANTHROPIC_API_KEY and records each model result separately.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from examples.adapters.anthropic_adapter import AnthropicAdapter
from runtime.oppai_runtime_flow import execute
from runtime.protocol_loader import load_matome

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_PATHS = (
    ROOT / "protocols/language/3d-pruim.yaml",
    ROOT / "protocols/language/anmon-layer-reverse.yaml",
    ROOT / "protocols/language/cognitive-echolocalization-hypothesis-v0.1.yaml",
    ROOT / "protocols/language/thread-rpg-v3.2.yaml",
)


def main() -> int:
    text = sys.stdin.read().strip()
    if not text:
        raise SystemExit("Provide one Landscape/task text on stdin.")

    adapter = AnthropicAdapter()
    runs = []
    for path in PROTOCOL_PATHS:
        artifact = load_matome(path)
        result = execute(text, adapter, protocol=artifact.protocol_id)
        runs.append(
            {
                "protocol_path": str(path.relative_to(ROOT)),
                "protocol_id": artifact.protocol_id,
                "version": artifact.version,
                "input": result["input"],
                "output": result["output"],
                "observation": result["observation"],
                "evidence": result["evidence"],
            }
        )

    print(
        json.dumps(
            {
                "experiment": "language-protocol-real-model-001",
                "raw_input": text,
                "runs": runs,
                "interpretation": {
                    "protocol_effect": "not_claimed",
                    "quality_comparison": "not_claimed",
                    "personality_comparison": "not_claimed",
                    "cognitive_echolocalization_verification": "not_claimed",
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
