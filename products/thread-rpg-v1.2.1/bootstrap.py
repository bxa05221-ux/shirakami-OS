"""Fail-closed, local-Git bootstrap verification for stable ThreadRPG v1.2.1.

This utility verifies repository objects only.  It does not launch ThreadRPG,
call a model, or claim that a natural-language activation was executed.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import subprocess
import sys


ENTRY_PATH = "products/thread-rpg-v1.2.1/START.md"
DEPENDENCY_PATH = "protocols/thread-rpg-v1.2.1.yaml"
EXPECTED_VERSION = "1.2.1"


@dataclass(frozen=True)
class BootstrapReport:
    repository: str
    requested_commit: str
    resolved_commit: str | None
    entry_path: str
    entry_blob_sha: str | None
    dependency_path: str
    dependency_blob_sha: str | None
    protocol_version: str | None
    verified: bool
    failure: str | None


def _git(repository: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True, capture_output=True, text=True, encoding="utf-8",
    )
    return completed.stdout.strip()


def _protocol_version(text: str) -> str | None:
    match = re.search(r"^  version:\s*['\"]?([^\s'\"]+)", text, re.MULTILINE)
    return match.group(1) if match else None


def verify_repository(repository: str | Path, commit: str) -> BootstrapReport:
    """Return same-commit evidence or a failure report without inference."""
    repo = Path(repository)
    base = dict(repository=str(repo), requested_commit=commit, resolved_commit=None,
                entry_path=ENTRY_PATH, entry_blob_sha=None,
                dependency_path=DEPENDENCY_PATH, dependency_blob_sha=None,
                protocol_version=None, verified=False, failure=None)
    try:
        resolved = _git(repo, "rev-parse", f"{commit}^{{commit}}")
        entry_blob = _git(repo, "rev-parse", f"{resolved}:{ENTRY_PATH}")
        dependency_blob = _git(repo, "rev-parse", f"{resolved}:{DEPENDENCY_PATH}")
        entry = _git(repo, "show", f"{resolved}:{ENTRY_PATH}")
        dependency = _git(repo, "show", f"{resolved}:{DEPENDENCY_PATH}")
        version = _protocol_version(dependency)
        if not entry.startswith("# ThreadRPG v1.2.1"):
            raise ValueError("entry guide identity mismatch")
        if version != EXPECTED_VERSION:
            raise ValueError(f"protocol version must be {EXPECTED_VERSION}")
        return BootstrapReport(**(base | {"resolved_commit": resolved,
            "entry_blob_sha": entry_blob, "dependency_blob_sha": dependency_blob,
            "protocol_version": version, "verified": True}))
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        return BootstrapReport(**(base | {"failure": str(error)}))


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: bootstrap.py <repository> <immutable-commit>", file=sys.stderr)
        return 2
    report = verify_repository(argv[1], argv[2])
    print(json.dumps(asdict(report), ensure_ascii=False, sort_keys=True))
    return 0 if report.verified else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
