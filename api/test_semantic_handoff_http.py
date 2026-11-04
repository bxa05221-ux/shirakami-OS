from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from api.http import ShirakamiHTTPTransport
from runtime.evolution_bridge import ContextSnapshot
from runtime.evolution_pipeline import EvidenceDrivenRuntime
from runtime.prototype import Transition


def test_semantic_handoff_http_exposes_lineage() -> None:
    runtime = EvidenceDrivenRuntime()

    def protocol(_: Any) -> Transition:
        return Transition(kind="semantic.handoff", data={"ok": True})

    api = ShirakamiHTTPTransport(
        api=None,
        protocol_registry={"semantic.handoff": protocol},
    )
    api.api.runtime = runtime

    api.api.observe(
        {},
        ContextSnapshot(
            protocol_id="semantic.handoff",
            landscape={},
            metadata={},
        ),
    )
    api.api.analyze("semantic.handoff", protocol_exists=True)

    result = api.api.execute(
        protocol,
        "semantic.handoff",
        {"input": "lineage"},
        handoff_id="HANDOFF-HTTP-001",
        project="Shirakami",
        objective="semantic handoff",
        protocol_ids=("semantic.handoff",),
        verification_scope=("execution",),
    )

    client = TestClient(api.create_app())
    response = client.get(f"/v1/semantic-handoff/{result['trace_id']}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["handoff_id"] == "HANDOFF-HTTP-001"
    assert payload["trace_id"] == result["trace_id"]
    assert payload["execution_id"] == result["execution_id"]
    assert payload["evidence_ids"] == result["evidence_ids"]
    assert payload["human_gate_required"] is True
    assert payload["execution_authorized"] is False
    assert payload["publish_authorized"] is False
    assert payload["merge_authorized"] is False


def test_semantic_handoff_http_returns_404_for_unknown_trace() -> None:
    client = TestClient(ShirakamiHTTPTransport().create_app())
    response = client.get("/v1/semantic-handoff/UNKNOWN")

    assert response.status_code == 404
