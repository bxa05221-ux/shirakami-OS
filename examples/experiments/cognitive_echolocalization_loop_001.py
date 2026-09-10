"""Minimal cognitive-echo loop observation experiment.

This experiment observes a two-turn projection/echo/re-projection loop
without adding cognitive-echolocalization semantics to Runtime Core.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from runtime.oppai_runtime_flow import execute

PROTOCOL = "shirakami-short-group-scene-v32"


class EchoAdapter:
    """Deterministic adapter used to observe the loop without an external API."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def __call__(self, input_text: str, protocol: str) -> str:
        self.calls.append({"input": input_text, "protocol": protocol})
        return f"echo-{len(self.calls)}: {input_text}"


def run(text: str) -> dict[str, Any]:
    adapter = EchoAdapter()

    first = execute(text, adapter, protocol=PROTOCOL)
    second_input = f"前の反応を受けて再投射: {first['output']}"
    second = execute(second_input, adapter, protocol=PROTOCOL)

    return {
        "experiment": "cognitive-echolocalization-loop-001",
        "protocol": PROTOCOL,
        "loop": {
            "turns": 2,
            "projection": text,
            "echo": first["output"],
            "re_projection": second_input,
            "echo_2": second["output"],
        },
        "observations": [first["observation"], second["observation"]],
        "evidence": [first["evidence"], second["evidence"]],
        "adapter_calls": adapter.calls,
        "interpretation": "not_claimed",
        "cognitive_echolocalization_semantics": "research_only",
    }


def main() -> None:
    text = sys.stdin.read().strip()
    if not text:
        raise SystemExit("Provide Landscape/task text on stdin.")
    print(json.dumps(run(text), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
