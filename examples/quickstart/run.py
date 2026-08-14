#!/usr/bin/env python3
"""Runnable Shirakami OS β0.1 Quickstart.

Matome YAML -> Protocol IR -> generic Protocol bridge -> Runtime -> Evidence -> Landscape State.
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
from protocol_bridge import protocol_from_ir
from protocol_loader import load_matome
from prototype import Runtime


def main() -> int:
    quickstart = Path(__file__).parent
    protocol_path = quickstart / "protocol.yaml"
    input_path = quickstart / "input.yaml"

    if not protocol_path.exists() or not input_path.exists():
        print("ERROR: quickstart files are missing")
        return 1

    try:
        protocol = load_matome(protocol_path)
    except Exception as exc:
        print(f"ERROR: Protocol load failed: {exc}")
        return 1

    print(f"Protocol loaded: {protocol.title} v{protocol.version}")
    input_data = {"message": "Hello Shirakami"}

    result = Runtime().execute(
        protocol.protocol_id,
        protocol_from_ir(protocol),
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
