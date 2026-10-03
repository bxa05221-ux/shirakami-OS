"""Pytest bootstrap for repository-local package boundaries."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_API_DIR = _ROOT / "api"
_API_INIT = _API_DIR / "__init__.py"

# The legacy suite used to prepend runtime/ to sys.path. That makes
# runtime/api.py shadow the repository-level api/ package. Keep the
# repository root authoritative instead.
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


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
