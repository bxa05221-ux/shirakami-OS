"""Tests for the HTTP transport boundary alpha 0.1."""

from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from api.http import create_app
from runtime.api import ShirakamiAPI
from runtime.evolution_pipeline import EvidenceDrivenRuntime
from runtime.prototype import Transition


def _protocol(_: Any) -> Transition:
    return Transition(kind="http.example", data={"changed": True})


def _client() -> TestClient:
    return TestClient(
        create_app(
            ShirakamiAPI(EvidenceDrivenRuntime()),
            {"http.example": _protocol},
        )
    )


def _context() -> dict[str, Any]:
    return {
        "protocol_id": "http.example",
        "landscape": {"topic": "ui-for-ai"},
        "metadata": {"source": "http-test"},
    }


def _boundary_context() -> dict[str, Any]:
    return {
        "handoff_id": "SH-HO-20260925-001",
        "project": "Shirakami Project",
        "objective": "Validate the API boundary",
        "protocol_ids": ["http.example"],
        "evidence_ids": ["AGENT-COORDINATION-001"],
        "verification_scope": ["HTTP execution boundary"],
    }


def _execute_payload(**overrides: Any) -> dict[str, Any]:
    payload = {
        "protocol_id": "http.example",
        "input_data": {"x": 1},
        "handoff_id": "SH-HO-20260925-001",
        "trace_id": "TRACE-HTTP-001",
        "evidence_ids": ["AGENT-COORDINATION-001"],
        "boundary_context": _boundary_context(),
    }
    payload.update(overrides)
    return payload


def test_health() -> None:
    response = _client().get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_observe_and_evidence_are_json_transport() -> None:
    client = _client()
    response = client.post(
        "/v1/observe",
        json={
            "observation": {"signal": "hello"},
            "context": _context(),
            "handoff_id": "SH-HO-20260925-001",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["state"] == "EVIDENCE"
    assert any(item["signals"] == ["CONTEXT_SNAPSHOT"] for item in body["evidence"])

    evidence = client.get("/v1/evidence", params={"signal": "CONTEXT_SNAPSHOT"})
    assert evidence.status_code == 200
    assert evidence.json()


def test_approval_cannot_be_inferred_over_http() -> None:
    client = _client()
    client.post(
        "/v1/observe",
        json={
            "observation": {},
            "context": _context(),
            "handoff_id": "SH-HO-20260925-001",
        },
    )
    client.post(
        "/v1/analyze",
        json={
            "protocol_id": "http.new",
            "protocol_exists": False,
            "diff_ref": "diff-http-1",
        },
    )

    denied = client.post(
        "/v1/approve",
        json={"approved": True, "reviewer": "human"},
    )
    assert denied.status_code == 200
    assert denied.json()["accepted"] is False

    approved = client.post(
        "/v1/approve",
        json={
            "approved": True,
            "reviewer": "human",
            "human_authorized": True,
        },
    )
    assert approved.status_code == 200
    assert approved.json()["accepted"] is True


def test_execute_requires_registered_protocol() -> None:
    client = _client()
    missing = client.post(
        "/v1/execute",
        json={
            "protocol_id": "unknown",
            "input_data": {},
            "handoff_id": "SH-HO-20260925-001",
            "evidence_ids": ["AGENT-COORDINATION-001"],
            "boundary_context": {
                **_boundary_context(),
                "protocol_ids": ["unknown"],
            },
        },
    )
    assert missing.status_code == 404

    client.post(
        "/v1/observe",
        json={
            "observation": {},
            "context": _context(),
            "handoff_id": "SH-HO-20260925-001",
        },
    )
    client.post(
        "/v1/analyze",
        json={"protocol_id": "http.example", "protocol_exists": True},
    )
    executed = client.post("/v1/execute", json=_execute_payload())
    assert executed.status_code == 200
    assert executed.json()["status"] == "completed"


def test_execution_handle_round_trip_and_verify() -> None:
    client = _client()
    client.post(
        "/v1/observe",
        json={
            "observation": {},
            "context": _context(),
            "handoff_id": "SH-HO-20260925-001",
        },
    )
    client.post(
        "/v1/analyze",
        json={"protocol_id": "http.example", "protocol_exists": True},
    )
    executed = client.post("/v1/execute", json=_execute_payload())
    assert executed.status_code == 200
    execution_id = executed.json()["execution_id"]
    status = client.get(f"/v1/executions/{execution_id}")
    assert status.status_code == 200
    assert status.json()["execution_id"] == execution_id
    verified = client.post(
        f"/v1/executions/{execution_id}/verify",
        json={"expected_transition_kind": "http.example"},
    )
    assert verified.status_code == 200
    assert verified.json()["status"] == "pass"


def test_unknown_execution_handle_fails_closed() -> None:
    client = _client()
    assert client.get("/v1/executions/unknown").status_code == 404
    assert client.post("/v1/executions/unknown/verify", json={}).status_code == 404


def test_http_trace_is_retrievable_after_execution() -> None:
    client = _client()
    client.post(
        "/v1/observe",
        json={"observation": {}, "context": _context(), "handoff_id": "SH-HO-20260925-001"},
    )
    client.post(
        "/v1/analyze",
        json={"protocol_id": "http.example", "protocol_exists": True},
    )
    executed = client.post("/v1/execute", json=_execute_payload())
    assert executed.status_code == 200
    trace_id = executed.json()["trace_id"]

    trace = client.get(f"/v1/traces/{trace_id}")
    assert trace.status_code == 200
    body = trace.json()
    assert body["trace_id"] == trace_id
    assert body["execution_id"] == executed.json()["execution_id"]
    assert body["handoff_id"] == "SH-HO-20260925-001"
    assert body["evidence_ids"] == ["AGENT-COORDINATION-001"]
    assert body["execution_authorized"] is False
    assert body["publish_authorized"] is False
    assert body["merge_authorized"] is False
    assert body["human_gate_required"] is True


def test_unknown_trace_fails_closed() -> None:
    client = _client()
    assert client.get("/v1/traces/unknown").status_code == 404


def test_http_round_trip_preserves_trace_metadata_without_authority() -> None:
    client = _client()
    client.post(
        "/v1/observe",
        json={
            "observation": {},
            "context": _context(),
            "handoff_id": "SH-HO-20260925-001",
        },
    )
    client.post(
        "/v1/analyze",
        json={"protocol_id": "http.example", "protocol_exists": True},
    )
    executed = client.post("/v1/execute", json=_execute_payload())
    assert executed.status_code == 200
    body = executed.json()
    assert body["handoff_id"] == "SH-HO-20260925-001"
    assert body["trace_id"] == "TRACE-HTTP-001"
    assert body["evidence_ids"] == ["AGENT-COORDINATION-001"]
    assert body["execution_authorized"] is False
    assert body["publish_authorized"] is False
    assert body["merge_authorized"] is False
    assert body["human_gate_required"] is True

    stored = client.get(f"/v1/executions/{body['execution_id']}")
    assert stored.status_code == 200
    assert stored.json()["handoff_id"] == "SH-HO-20260925-001"
    assert stored.json()["trace_id"] == "TRACE-HTTP-001"
    assert stored.json()["evidence_ids"] == ["AGENT-COORDINATION-001"]


def test_http_rejects_handoff_id_drift_at_boundary() -> None:
    client = _client()
    payload = _execute_payload(handoff_id="SH-HO-DRIFT-001")
    response = client.post("/v1/execute", json=payload)
    assert response.status_code == 422
    assert "handoff_id mismatch" in response.json()["detail"]


def test_http_rejects_evidence_id_drift_at_boundary() -> None:
    client = _client()
    payload = _execute_payload(evidence_ids=["EVIDENCE-DRIFT-001"])
    response = client.post("/v1/execute", json=payload)
    assert response.status_code == 422
    assert "evidence_ids mismatch" in response.json()["detail"]


def test_http_rejects_undeclared_protocol_at_boundary() -> None:
    client = _client()
    payload = _execute_payload(
        protocol_id="http.other",
        boundary_context={
            **_boundary_context(),
            "protocol_ids": ["http.example"],
        },
    )
    response = client.post("/v1/execute", json=payload)
    assert response.status_code == 422
    assert "protocol_id is not declared" in response.json()["detail"]


def test_http_witness_is_retrievable_after_execution() -> None:
    client = _client()
    executed = client.post("/v1/execute", json=_execute_payload())
    assert executed.status_code == 200
    body = executed.json()

    witness = client.get(f"/v1/witnesses/{body['trace_id']}")
    assert witness.status_code == 200
    observed = witness.json()
    assert observed["witness_id"].startswith("WITNESS-")
    assert observed["trace_id"] == body["trace_id"]
    assert observed["execution_id"] == body["execution_id"]
    assert observed["handoff_id"] == body["handoff_id"]
    assert observed["evidence_ids"] == body["evidence_ids"]
    assert observed["execution_authorized"] is False
    assert observed["publish_authorized"] is False
    assert observed["merge_authorized"] is False
    assert observed["human_gate_required"] is True


def test_unknown_witness_fails_closed() -> None:
    client = _client()
    assert client.get("/v1/witnesses/unknown").status_code == 404
