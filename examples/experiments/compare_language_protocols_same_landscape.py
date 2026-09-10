"""Compare multiple language protocols on the same Landscape input.

The experiment loads protocol IDs from the actual Matome artifacts and then
passes the same normalized input through the existing Runtime/Adapter boundary.
It records identifier collisions rather than silently resolving them.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from runtime.oppai_runtime_flow import execute
from runtime.protocol_loader import load_matome

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL_PATHS = (
    ROOT / "protocols/language/3d-pruim.yaml",
    ROOT / "protocols/language/anmon-layer-reverse.yaml",
    ROOT / "protocols/language/cognitive-echolocalization-hypothesis-v0.1.yaml",
    ROOT / "protocols/language/thread-rpg-v3.2.yaml",
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
    artifacts = [(path, load_matome(path)) for path in PROTOCOL_PATHS]
    results = [
        execute(text, adapter, protocol=artifact.protocol_id)
        for _, artifact in artifacts
    ]
    protocol_ids = [artifact.protocol_id for _, artifact in artifacts]

    collisions: dict[str, list[str]] = {}
    for path, artifact in artifacts:
        collisions.setdefault(artifact.protocol_id, []).append(str(path.relative_to(ROOT)))
    collision_groups = {key: value for key, value in collisions.items() if len(value) > 1}

    return {
        "experiment_id": "language-protocol-same-landscape-001",
        "raw_input": text,
        "protocols": [
            {
                "path": str(path.relative_to(ROOT)),
                "title": artifact.title,
                "version": artifact.version,
                "protocol_id": artifact.protocol_id,
                "pipeline": [step["phase"] for step in artifact.pipeline],
            }
            for path, artifact in artifacts
        ],
        "results": results,
        "comparison": {
            "same_raw_input": True,
            "same_canonical_input": len({r["input"] for r in results}) == 1,
            "distinct_protocol_ids": len(set(protocol_ids)) == len(protocol_ids),
            "protocol_id_collision_count": len(protocol_ids) - len(set(protocol_ids)),
            "protocol_id_collision_groups": collision_groups,
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
