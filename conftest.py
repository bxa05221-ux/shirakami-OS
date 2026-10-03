"""Pytest bootstrap for repository-local package boundaries."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_API_DIR = _ROOT / "api"
_API_INIT = _API_DIR / "__init__.py"
_RUNTIME_DIR = _ROOT / "runtime"

# Keep the repository root authoritative so runtime/api.py cannot shadow
# the repository-level api/ package.
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# Legacy runtime modules still use top-level imports (e.g. `from evidence import ...`).
# Append runtime after the repository root so those imports remain available
# without allowing runtime/api.py to shadow api/.
if str(_RUNTIME_DIR) not in sys.path:
    sys.path.append(str(_RUNTIME_DIR))


def _ensure_root_api_package() -> None:
    current = sys.modules.get("api")
    if current is not None and hasattr(current, "__path__"):
        return

    spec = importlib.util.spec_from_file_location(
        "api",
        _API_INIT,
        submodule_search_locations=[str(_API_DIR)],
    )
    if spec is None or spec.loader is None:
        raise ImportError("could not initialize repository api package")

    module = importlib.util.module_from_spec(spec)
    sys.modules["api"] = module
    spec.loader.exec_module(module)


_ensure_root_api_package()
