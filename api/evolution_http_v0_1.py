"""HTTP route factory for Evolution API v0.1.

FastAPI is optional at import time so the Runtime remains usable without the
HTTP dependency. The route itself only delegates to the thin API adapter.
"""

from __future__ import annotations

from typing import Any, Mapping

from api.evolution_v0_1 import execute_evolution_v0_1
from runtime.backend import Backend


def build_evolution_router(backend: Backend):
    """Return a FastAPI router exposing POST /v0.1/evolution/execute."""
    from fastapi import APIRouter

    router = APIRouter()

    @router.post("/v0.1/evolution/execute")
    def execute(payload: Mapping[str, Any]) -> dict[str, Any]:
        return execute_evolution_v0_1(backend, payload)

    return router
