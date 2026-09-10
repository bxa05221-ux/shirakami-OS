"""Compare multiple language protocols on the same Landscape input.

This experiment intentionally does not inject protocol YAML semantics into the
model prompt. The current Runtime contract passes the selected protocol ID
alongside the canonical input. The purpose is to observe that boundary before
making any semantic-prompting change.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from runtime.oppai_runtime_flow import execute

PROTOCOLS = (
    "shirakami-3d-pruim",
    "shirakami-anmon-layer-reverse",
    "shirakami-cognitive-echolocalization-hypothesis-v0.1",
    "shirakami-thread-rpg-v3.2",
)


class ComparisonAdapter:
    """Deterministic adapter that records the Runtime boundary."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def __call__(self, input_text: str, protocol: str) -> str:
        self.calls.append({"input": input_text, "protocol": protocol})
        return f"observed adapter call for {protocol}"


def run(text: str) -> dict[str, Any]:
    adapter = ComparisonAdapter()
    results = [execute(text, adapter, protocol=protocol) for protocol in PROTOCOLS]

    return {
        "experiment_id": "language-protocol-same-landscape-001",
        "raw_input": text,
        "protocols": list(PROTOCOLS),
        "results": results,
        "comparison": {
            "same_raw_input": True,
            "same_canonical_input": len({r["input"] for r in results}) == 1,
            "distinct_protocol_ids": len({r["protocol"] for r in results}) == len(PROTOCOLS),
            "semantic_effect_conclusion": "not_claimed",
            "ai_behavior_conclusion": "not_claimed",
            "research_status": "observation_only",
        },
        "adapter_calls": adapter.calls,
    }


def main() -> None:
    text = sys.stdin.read().strip()
    if not text:
        raise SystemExit("Provide a Landscape/task text on stdin.")
    print(json.dumps(run(text), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
