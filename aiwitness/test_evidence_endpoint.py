from __future__ import annotations

import sys
import types
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

_REPO_ROOT = Path(__file__).resolve().parents[1]
_api_package = types.ModuleType("api")
_api_package.__path__ = [str(_REPO_ROOT / "api")]
sys.modules["api"] = _api_package

from api.http import create_app
from runtime.api import ShirakamiAPI
from runtime.evolution_bridge import ContextSnapshot
from runtime.evolution_pipeline import EvidenceDrivenRuntime
from runtime.prototype import Transition


def _protocol(_: Any) -> Transition:
    return Transition(kind="evidence.endpoint", data={"changed": True})


def test_evidence_can_be_resolved_by_stable_id() -> None:
    api = ShirakamiAPI(EvidenceDrivenRuntime())
    api.observe({}, ContextSnapshot(protocol_id="evidence.endpoint", landscape={}, metadata={}))
    api.analyze("evidence.endpoint", protocol_exists=True)
    client = TestClient(create_app(api, {"evidence.endpoint": _protocol}))

    executed = client.post("/v1/execute", json={
        "protocol_id": "evidence.endpoint",
        "input_data": {},
        "handoff_id": "SH-HO-EVIDENCE-001",
        "evidence_ids": [],
        "boundary_context": {
            "handoff_id": "SH-HO-EVIDENCE-001",
            "project": "Shirakami",
            "objective": "stable evidence retrieval",
            "protocol_ids": ["evidence.endpoint"],
            "evidence_ids": [],
            "verification_scope": ["evidence"],
        },
    })
    assert executed.status_code == 200
    evidence_id = executed.json()["evidence_ids"][0]

    response = client.get(f"/v1/evidence/{evidence_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["evidence_id"] == evidence_id
    assert body["protocol_id"] == "evidence.endpoint"

    assert client.get("/v1/evidence/UNKNOWN-EVIDENCE").status_code == 404
