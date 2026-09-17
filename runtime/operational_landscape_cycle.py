"""Read-only operational Landscape cycle entrypoint."""

import json
import os
import sys
from collections.abc import Mapping

from .live_github_probe import read_live_repository_landscape
from .landscape import LandscapeState
from .observable_execution import execute_observably
from .prototype import Runtime, example_protocol


def _json_safe(value):
    """Convert immutable container boundaries into JSON-compatible values."""
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set, frozenset)):
        return [_json_safe(item) for item in value]
    return value


def main() -> int:
    if os.environ.get("SHIRAKAMI_LIVE_GITHUB_TEST") != "1":
        print("SHIRAKAMI_LIVE_GITHUB_TEST=1 is required", file=sys.stderr)
        return 2
    token = os.environ.get("SHIRAKAMI_GITHUB_TOKEN")
    if not token:
        print("SHIRAKAMI_GITHUB_TOKEN is required", file=sys.stderr)
        return 2
    owner = os.environ.get("SHIRAKAMI_GITHUB_OWNER", "bxa05221-ux")
    repo = os.environ.get("SHIRAKAMI_GITHUB_REPO", "shirakami-OS")
    branch = os.environ.get("SHIRAKAMI_GITHUB_BRANCH", "main")
    observed = read_live_repository_landscape(owner, repo, lambda: token, branch=branch)
    state = LandscapeState.from_snapshot(observed)
    result = execute_observably(
        state, Runtime(), "example.protocol", example_protocol,
        {"operation": "operational-observation"},
    )
    print(json.dumps(_json_safe({
        "before_state": result.before_state,
        "evidence": {
            "protocol_id": result.evidence.protocol_id,
            "transition_kind": result.evidence.transition_kind,
            "status": result.evidence.status,
        },
        "after_state": result.after_state,
        "observation": result.observation,
    }), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
