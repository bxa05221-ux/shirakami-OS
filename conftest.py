"""Pytest path configuration for the legacy runtime test suite."""

import sys
from pathlib import Path

RUNTIME_DIR = Path(__file__).resolve().parent / "runtime"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))
