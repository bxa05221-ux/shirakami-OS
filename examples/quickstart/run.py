#!/usr/bin/env python3
"""Runnable Shirakami OS β0.1 Quickstart.

This example uses the existing β0.1 Runtime vertical slice directly:
Protocol -> Execution -> Transition -> Evidence -> Landscape State.
No GitHub credentials or external packages are required.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "runtime"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from evidence import capture_evidence
from landscape import LandscapeState
from prototype import Runtime, example_protocol


def main() -> int:
    quickstart = Path(__file__).parent
    protocol_path = quickstart / "protocol.yaml"
    input_path = quickstart / "input.yaml"

    if not protocol_path.exists() or not input_path.exists():
        print("ERROR: quickstart files are missing")
        return 1

    print("Protocol loaded")
    input_data = {"message": "Hello Shirakami"}

    result = Runtime().execute(
        "quickstart.observation",
        example_protocol,
        input_data,
    )
    print("Observation captured")

    evidence = capture_evidence(result)
    print("Transition created")
    print("Evidence captured")

    landscape = LandscapeState.empty()
    landscape.apply_evidence(evidence)
    print("Landscape State exposed")
    print(landscape.snapshot())

    if result.status != "completed":
        print("\nFAILED")
        return 1

    print("\nSUCCESS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
