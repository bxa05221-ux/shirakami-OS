"""Pytest path configuration for the legacy runtime test suite."""

import sys
from pathlib import Path

RUNTIME_DIR = Path(__file__).resolve().parent / "runtime"
if str(RUNTIME_DIR) not in sys.path:
    # Keep the top-level api package ahead of the legacy runtime/api.py module.
    # Direct imports such as `from prototype import Transition` remain available.
    sys.path.append(str(RUNTIME_DIR))
