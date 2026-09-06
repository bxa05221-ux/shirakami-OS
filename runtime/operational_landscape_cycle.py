"""Small read-only operational cycle over a live repository Landscape observation."""

from __future__ import annotations

import json
import os
import sys

from .live_github_probe import read_live_repository_landscape
from .landscape import LandscapeState
from .observable_execution import execute_observably
from .prototype import Runtime, example_protocol


def run() -> int:
    if os.getenv("SHIRAKAMI_LIVE_GITHUB_TEST") != "1":
        print("live Landscape cycle is disabled; set SHIRAKAMI_LIVE_GITHUB_TEST=1", file=sys.stderr)
        return 2

    token = os.getenv("SHIRAKAMI_GITHUB_TOKEN", "")
    if not token:
        print("SHIRAKAMI_GITHUB_TOKEN is required", file=sys.stderr)
        return 2

    owner = os.getenv("SHIRAKAMI_GITHUB_OWNER", "bxa05221-ux")
    repo = os.getenv("SHIRAKAMI_GITHUB_REPO", "shirakami-OS")
    branch = os.getenv("SHIRAKAMI_GITHUB_BRANCH", "main")

    observed = read_live_repository_landscape(owner, repo, lambda: token, branch=branch)
    state = LandscapeState.from_snapshot(observed)
    result = execute_observably(
        state,
        Runtime(),
        "example.protocol",
        example_protocol,
        {"operation": "operational-observation"},
    )
    print(
        json.dumps(
            {
                "before_state": result.before_state,
                "evidence": {
                    "protocol_id": result.evidence.protocol_id,
                    "transition_kind": result.evidence.transition_kind,
                    "status": result.evidence.status,
                },
                "after_state": result.after_state,
                "observation": result.observation,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
