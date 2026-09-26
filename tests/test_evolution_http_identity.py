"""Phase 2 vertical-slice verification for SemanticHandoff → Evidence."""

from api.evolution_v0_1 import execute_evolution_v0_1
from runtime.backend import BackendResponse


class RecordingBackend:
    backend_id = "recording:v0.1"

    def __init__(self):
        self.handoff = None

    def execute(self, handoff):
        self.handoff = dict(handoff)
        return BackendResponse(
            backend_id=self.backend_id,
            status="completed",
            payload={"observed_handoff": dict(handoff)},
        )


def test_semantic_handoff_identity_survives_runtime_evidence_boundary():
    backend = RecordingBackend()
    handoff = {
        "request_id": "req-phase2-001",
        "evidence_ids": ["e-001", "e-002"],
        "interpretation_id": "i-001",
        "decision_id": "d-001",
        "gate_id": "g-001",
        "evidence_store": {
            "e-001": {"evidence_id": "e-001", "value": "alpha"},
            "e-002": {"evidence_id": "e-002", "value": "beta"},
            "e-unrequested": {"evidence_id": "e-unrequested", "value": "exclude"},
        },
        "payload": {"task": "identity-round-trip"},
        "authority": "not_inferred",
    }

    result = execute_evolution_v0_1(backend, handoff)
    observed = result["transition_data"]["payload"]["observed_handoff"]

    assert observed["request_id"] == handoff["request_id"]
    assert observed["evidence_ids"] == handoff["evidence_ids"]
    assert observed["interpretation_id"] == handoff["interpretation_id"]
    assert observed["decision_id"] == handoff["decision_id"]
    assert observed["gate_id"] == handoff["gate_id"]
    assert observed["context_lineage"]["evidence_ids"] == handoff["evidence_ids"]
    assert "evidence_store" not in observed
    assert result["transition_data"]["authority"] == "not_inferred"
    assert result["evidence_id"]


def test_unrequested_evidence_does_not_cross_context_bundle_boundary():
    backend = RecordingBackend()
    handoff = {
        "request_id": "req-phase2-002",
        "evidence_ids": ["e-001"],
        "evidence_store": {
            "e-001": {"evidence_id": "e-001", "value": "admit"},
            "e-002": {"evidence_id": "e-002", "value": "exclude"},
        },
    }

    execute_evolution_v0_1(backend, handoff)
    admitted = backend.handoff["context_bundle"]["evidence"]
    admitted_ids = [item["evidence_id"] for item in admitted]

    assert admitted_ids == ["e-001"]
    assert "e-002" not in admitted_ids
