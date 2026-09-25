from fastapi.testclient import TestClient

from api.http import create_app


def test_comparative_trace_http_boundary_preserves_reviewer_context() -> None:
    client = TestClient(create_app(api_key=None))

    response = client.post(
        "/v1/reviews/register",
        json={
            "project_id": "project-http-e2e",
            "reviewer_id": "reviewer-a",
            "matome_yaml": "matome: perspective-a",
            "metadata": {"role": "research"},
        },
    )
    assert response.status_code == 200

    response = client.post(
        "/v1/reviews/register",
        json={
            "project_id": "project-http-e2e",
            "reviewer_id": "reviewer-b",
            "matome_yaml": "matome: perspective-b",
        },
    )
    assert response.status_code == 200

    for reviewer_id, evidence_ids, finding in (
        ("reviewer-a", ["E1", "E2"], "x"),
        ("reviewer-b", ["E1", "E3"], "y"),
    ):
        response = client.post(
            "/v1/reviews/submit",
            json={
                "project_id": "project-http-e2e",
                "reviewer_id": reviewer_id,
                "observation": {"finding": finding},
                "evidence_ids": evidence_ids,
                "proposal": {"next": "inspect"},
            },
        )
        assert response.status_code == 200

    response = client.post(
        "/v1/reviews/comparative",
        json={"project_id": "project-http-e2e"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["shared_evidence_ids"] == ["E1"]
    assert body["divergent_evidence_ids"] == ["E2", "E3"]
    assert {item["reviewer_id"] for item in body["reviewers"]} == {
        "reviewer-a",
        "reviewer-b",
    }
    assert body["decision"] is None
    assert body["human_gate_required"] is True

    response = client.get("/v1/reviews/comparative/project-http-e2e")
    assert response.status_code == 200
    assert response.json()["decision"] is None


def test_comparative_trace_http_boundary_rejects_unknown_project() -> None:
    client = TestClient(create_app(api_key=None))
    response = client.post(
        "/v1/reviews/comparative",
        json={"project_id": "unknown"},
    )
    assert response.status_code == 404
