"""HTTP integration tests for machine-checkable provenance."""

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
from aiwitness.traceability import validate_traceability


def _protocol(_: Any) -> Transition:
    return Transition(kind="http.traceability", data={"changed": True})


def _client() -> TestClient:
    api = ShirakamiAPI(EvidenceDrivenRuntime())
    api.observe({}, ContextSnapshot(protocol_id="http.traceability", landscape={}, metadata={}))
    api.analyze("http.traceability", protocol_exists=True)
    return TestClient(create_app(api, {"http.traceability": _protocol}))


def _boundary() -> dict[str, Any]:
    return {
        "handoff_id": "SH-HO-20260925-001",
        "project": "Shirakami Project",
        "objective": "HTTP provenance chain",
        "protocol_ids": ["http.traceability"],
        "evidence_ids": ["AGENT-COORDINATION-001"],
        "verification_scope": ["HTTP provenance"],
    }


def test_http_execution_provenance_is_machine_checkable() -> None:
    client = _client()
    executed = client.post("/v1/execute", json={
        "protocol_id": "http.traceability", "input_data": {"x": 1},
        "handoff_id": "SH-HO-20260925-001", "trace_id": "TRACE-HTTP-CHAIN-001",
        "evidence_ids": ["AGENT-COORDINATION-001"], "boundary_context": _boundary(),
    })
    assert executed.status_code == 200
    body = executed.json()
    execution = client.get(f"/v1/executions/{body['execution_id']}").json()
    trace = client.get(f"/v1/traces/{body['trace_id']}").json()
    witness = client.get(f"/v1/witnesses/{body['trace_id']}").json()
    record = validate_traceability(execution=execution, trace=trace, witness=witness, evidence_ids=body["evidence_ids"])
    assert record.handoff_id == body["handoff_id"]
    assert record.execution_id == body["execution_id"]
    assert record.trace_id == body["trace_id"]
    assert record.evidence_ids == tuple(body["evidence_ids"])
    assert record.verification_status == "pending"


def test_http_provenance_chain_remains_checkable_after_verify() -> None:
    client = _client()
    executed = client.post("/v1/execute", json={
        "protocol_id": "http.traceability", "input_data": {},
        "handoff_id": "SH-HO-20260925-001", "trace_id": "TRACE-HTTP-CHAIN-002",
        "evidence_ids": ["AGENT-COORDINATION-001"], "boundary_context": _boundary(),
    })
    assert executed.status_code == 200
    body = executed.json()
    checked = client.post(f"/v1/executions/{body['execution_id']}/verify", json={"expected_transition_kind": "http.traceability"})
    assert checked.status_code == 200
    assert checked.json()["status"] == "pass"
    execution = client.get(f"/v1/executions/{body['execution_id']}").json()
    trace = client.get(f"/v1/traces/{body['trace_id']}").json()
    witness = client.get(f"/v1/witnesses/{body['trace_id']}").json()
    record = validate_traceability(execution=execution, trace=trace, witness=witness, evidence_ids=body["evidence_ids"])
    assert record.verification_status == "pass"
    assert trace["verification_status"] == witness["verification_status"] == "pass"
