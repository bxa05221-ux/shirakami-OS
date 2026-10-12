#!/usr/bin/env python3
"""Run the deterministic Shirakami OS contest prototype checks in order.

Install the verification dependencies first:
    python -m pip install pytest pyyaml fastapi pydantic httpx

Then run from the repository root:
    python scripts/contest_demo.py

This script deliberately does not call an external AI provider or require API keys.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    [sys.executable, "shirakami_os.py"],
    [sys.executable, "examples/evidence_route_demo.py"],
    [sys.executable, "-m", "pytest", "runtime", "tests", "-q"],
]


def main() -> int:
    for index, command in enumerate(COMMANDS, start=1):
        print(f"\n[{index}/{len(COMMANDS)}] {' '.join(command)}", flush=True)
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode != 0:
            print(
                f"FAILED: command {index} exited with status {result.returncode}.",
                file=sys.stderr,
                flush=True,
            )
            return result.returncode or 1
    print("\nPASS: all deterministic contest prototype checks completed.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
