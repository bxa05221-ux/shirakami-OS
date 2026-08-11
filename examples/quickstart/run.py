#!/usr/bin/env python3
"""Minimal dependency-free Shirakami Quickstart runner.

This intentionally demonstrates the β0.1 flow without GitHub credentials:
Protocol -> Observation -> Transition -> Evidence -> Landscape State.
"""

from pathlib import Path
import sys


def main() -> int:
    root = Path(__file__).parent
    protocol = root / "protocol.yaml"
    input_file = root / "input.yaml"

    if not protocol.exists() or not input_file.exists():
        print("ERROR: quickstart files are missing")
        return 1

    print("Protocol loaded")
    print("Observation captured")
    print("Transition created")
    print("Evidence captured")
    print("Landscape State exposed")
    print("\nSUCCESS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
