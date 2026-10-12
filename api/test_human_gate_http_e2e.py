"""HTTP E2E check for candidate execution across the Human Gate.

The provider callback is deterministic and credential-free. This verifies the
HTTP/runtime authority boundary; it does not claim a live external provider run.
"""

from fastapi.testclient import TestClient

from api.http import create_app
from runtime.prototype import Transition


API_KEY = "test-human-gate-key"
PROTOCOL_ID = "contest.candidate.fixture"
HANDOFF_ID = "SH-HO-CONTEST-HG-001"
TRACE_ID = "TRACE-CONTEST-HG-001"


def candidate_protocol(context):
    return Transition(
        kind="contest.human_gate.fixture",
        data={"input": dict(context.input)},
    )


def fixture_model_adapter(prompt, protocol_id):
    return {
        "provider": "deterministic-fixture",
        "output": prompt,
        "protocol_id": protocol_id,
    }


def test_http_candidate_requires_explicit_human_gate_before_execution():
    client = TestClient(
        create_app(
            protocol_registry={PROTOCOL_ID: candidate_protocol},
            api_key=API_KEY,
            model_adapter=fixture_model_adapter,
        )
    )
    headers = {"X-API-Key": API_KEY}

    observed = client.post(
        "/v1/observe",
        headers=headers,
        json={
            "observation": {"task": "contest prototype gate check"},
            "context": {
                "protocol_id": PROTOCOL_ID,
                "landscape": {"purpose": "verification"},
                "metadata": {"source": "human-gate-http-e2e"},
            },
            "handoff_id": HANDOFF_ID,
            "trace_id": TRACE_ID,
            "evidence_ids": [],
        },
    )
    assert observed.status_code == 200, observed.text

    analyzed = client.post(
        "/v1/analyze",
        headers=headers,
        json={
            "protocol_id": PROTOCOL_ID,
            "protocol_exists": False,
            "diff_ref": "contest-prototype-fixture",
        },
    )
    assert analyzed.status_code == 200, analyzed.text

    execute_payload = {
        "protocol_id": PROTOCOL_ID,
        "input_data": {"text": "deterministic fixture prompt"},
        "handoff_id": HANDOFF_ID,
        "trace_id": TRACE_ID,
        "evidence_ids": [],
        "boundary_context": {
            "handoff_id": HANDOFF_ID,
            "project": "Shirakami contest prototype",
            "objective": "Verify candidate Human Gate boundary",
            "protocol_ids": [PROTOCOL_ID],
            "evidence_ids": [],
            "verification_scope": ["human_gate", "evidence", "trace"],
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
            "human_gate_required": True,
        },
    }

    # A caller cannot approve by merely requesting approval without explicit
    # human authorization, and execution stays blocked while review is pending.
    unauthorized_approval = client.post(
        "/v1/approve",
        headers=headers,
        json={"approved": True, "reviewer": "test", "human_authorized": False},
    )
    assert unauthorized_approval.status_code == 200, unauthorized_approval.text
    assert unauthorized_approval.json()["accepted"] is False
    assert unauthorized_approval.json()["state"] == "HUMAN_REVIEW"

    blocked = client.post("/v1/execute", headers=headers, json=execute_payload)
    assert blocked.status_code == 409, blocked.text
    assert "Human Gate approval required" in blocked.json()["detail"]

    approved = client.post(
        "/v1/approve",
        headers=headers,
        json={"approved": True, "reviewer": "human-reviewer", "human_authorized": True},
    )
    assert approved.status_code == 200, approved.text
    assert approved.json()["accepted"] is True
    assert approved.json()["state"] == "READY"

    executed = client.post("/v1/execute", headers=headers, json=execute_payload)
    assert executed.status_code == 200, executed.text
    body = executed.json()
    assert body["status"] == "completed"
    assert body["transition"]["kind"] == "contest.human_gate.fixture"
    assert body["trace_id"] == TRACE_ID
    assert body["evidence_ids"]
    assert body["execution_authorized"] is False
    assert body["publish_authorized"] is False
    assert body["merge_authorized"] is False
    assert body["human_gate_required"] is True

    evidence_id = body["evidence_ids"][0]
    evidence = client.get(f"/v1/evidence/{evidence_id}", headers=headers)
    assert evidence.status_code == 200, evidence.text
    evidence_body = evidence.json()
    assert evidence_body["model_output"] == {
        "provider": "deterministic-fixture",
        "output": "deterministic fixture prompt",
        "protocol_id": PROTOCOL_ID,
    }

    verified = client.post(
        f"/v1/executions/{body['execution_id']}/verify",
        headers=headers,
        json={"expected_transition_kind": "contest.human_gate.fixture"},
    )
    assert verified.status_code == 200, verified.text
    assert verified.json()["status"] == "pass"

    traceability = client.get(f"/v1/traceability/{TRACE_ID}", headers=headers)
    assert traceability.status_code == 200, traceability.text
    assert traceability.json()["valid"] is True
