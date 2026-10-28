"""Opt-in two-process HTTP integration with UMR's local mock engine only."""

import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time

import httpx
import pytest
from fastapi.testclient import TestClient

from api.http import create_app
from runtime.api import ShirakamiAPI
from runtime.thread_rpg_umr_adapter import create_thread_rpg_umr_adapter


@pytest.fixture(scope="module")
def mock_umr_url(tmp_path_factory):
    checkout = os.environ.get("SHIRAKAMI_UMR_CHECKOUT")
    if not checkout:
        pytest.skip("Set SHIRAKAMI_UMR_CHECKOUT to run the local UMR mock HTTP integration")
    root = Path(checkout).resolve()
    assert (root / "api" / "routes.py").is_file(), "UMR checkout is incomplete"
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    base_url = f"http://127.0.0.1:{port}"
    log_path = tmp_path_factory.mktemp("umr") / "startup.log"
    # UMR and Shirakami both have an api package; keep separate processes/cwds.
    env = {**os.environ, "PYTHONPATH": str(root), "PYTHONDONTWRITEBYTECODE": "1"}
    with log_path.open("w") as log:
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "api.routes:app", "--host", "127.0.0.1", "--port", str(port)],
            cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT,
        )
        try:
            deadline = time.monotonic() + 15
            with httpx.Client(trust_env=False, timeout=1) as client:
                while time.monotonic() < deadline:
                    assert process.poll() is None, log_path.read_text()
                    try:
                        response = client.get(base_url + "/health")
                        if response.status_code == 200 and response.json().get("status") == "ok":
                            break
                    except httpx.HTTPError:
                        pass
                    time.sleep(0.05)
                else:
                    pytest.fail("UMR readiness timeout: " + log_path.read_text())
            yield base_url
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


def payload():
    return {
        "task": {"question": "Compare interpretations without deciding"},
        "perspectives": [{"id": "A"}, {"id": "B"}],
        "context": {"source": "local-http-fixture"},
    }


def test_factory_and_endpoint_use_real_umr_http_without_promoting_outputs(mock_umr_url):
    api = ShirakamiAPI()
    before = api.runtime.store
    adapter = create_thread_rpg_umr_adapter(base_url=mock_umr_url, engine="mock")
    client = TestClient(create_app(api=api, api_key="test-key", thread_rpg_adapter=adapter))
    response = client.post(
        "/v1/thread-rpg/execute", headers={"X-API-Key": "test-key"}, json=payload(),
    )
    assert response.status_code == 200, response.text
    body = response.json()
    phase_results = [item[1] for item in body["trace"]]
    # UMR mock echoes the actual serialized request across the HTTP boundary.
    inputs = [json.loads(result["output"]["text"]) for result in phase_results]
    assert [item["task_input"]["phase"] for item in inputs] == [
        "independent_observation", "independent_observation", "conference", "matome",
    ]
    assert [len(item["previous_outputs"]) for item in inputs] == [0, 0, 2, 3]
    assert [item["task_input"]["perspective"]["id"] for item in inputs[:2]] == ["A", "B"]
    assert {item["perspective_id"] for item in inputs[2]["task_input"]["observations"]} == {"A", "B"}
    assert "conference" in inputs[3]["task_input"]
    assert all(item["context_bundle"]["source"] == "local-http-fixture" for item in inputs)
    assert body["record_status"] == "generated"
    assert body["trace_kind"] == "thread_rpg.phase_results"
    assert body["evidence_ids"] == []
    assert body["decision_authority"] is False
    assert body["execution_authorized"] is False
    assert api.runtime.store is before


def test_umr_rejected_engine_returns_502_without_recording_evidence(mock_umr_url):
    api = ShirakamiAPI()
    before = api.runtime.store
    adapter = create_thread_rpg_umr_adapter(base_url=mock_umr_url, engine="missing-fixture-engine")
    client = TestClient(create_app(api=api, thread_rpg_adapter=adapter))
    response = client.post("/v1/thread-rpg/execute", json=payload())
    assert response.status_code == 502
    assert api.runtime.store is before
