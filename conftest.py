"""Pytest path configuration for the legacy runtime test suite."""

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent
RUNTIME_DIR = REPOSITORY_ROOT / "runtime"
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(1, str(RUNTIME_DIR))
