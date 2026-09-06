"""Small operational entrypoint for a read-only GitHub Landscape observation.

Credentials are supplied by the process environment and are never persisted.
"""

from __future__ import annotations

import json
import os
import sys

from .live_github_probe import read_live_repository_landscape


def main() -> int:
    if os.getenv("SHIRAKAMI_LIVE_GITHUB_TEST") != "1":
        print("live GitHub read is disabled; set SHIRAKAMI_LIVE_GITHUB_TEST=1", file=sys.stderr)
        return 2

    token = os.getenv("SHIRAKAMI_GITHUB_TOKEN", "")
    if not token:
        print("SHIRAKAMI_GITHUB_TOKEN is required", file=sys.stderr)
        return 2

    owner = os.getenv("SHIRAKAMI_GITHUB_OWNER", "bxa05221-ux")
    repo = os.getenv("SHIRAKAMI_GITHUB_REPO", "shirakami-OS")
    branch = os.getenv("SHIRAKAMI_GITHUB_BRANCH", "main")

    result = read_live_repository_landscape(owner, repo, lambda: token, branch=branch)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
