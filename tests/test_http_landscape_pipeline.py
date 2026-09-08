from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "dogfight_scene.json"


def request_json(url: str, method: str = "GET", payload: dict | None = None) -> tuple[int, dict | list]:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    with urlopen(request, timeout=5) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def test_http_uses_real_landscape_pipeline() -> None:
    scene = json.loads(FIXTURE.read_text(encoding="utf-8"))
    process = subprocess.Popen(
        [sys.executable, "-m", "runtime.http_api"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(50):
            try:
                status, _ = request_json("http://127.0.0.1:8000/sessions")
                if status:
                    break
            except Exception:
                time.sleep(0.05)

        status, created = request_json(
            "http://127.0.0.1:8000/sessions",
            "POST",
            {
                "session_id": "dogfight-http-pipeline",
                "landscape_ref": "dogfight-fixture",
                "landscape": {"scene_id": scene["scene_id"], "type": scene["type"]},
                "sources": [
                    {
                        "id": "dogfight_scene",
                        "type": "implementation",
                        "path": "tests/fixtures/dogfight_scene.json",
                        "status": "active",
                        "authority": "test-fixture",
                    }
                ],
                "source_contents": {"dogfight_scene": scene},
            },
        )
        assert status == 201
        assert created["context"]["source_ids"] == ["dogfight_scene"]
        assert created["context"]["unresolved_questions"] == []

        status, turn = request_json(
            "http://127.0.0.1:8000/sessions/dogfight-http-pipeline/turns",
            "POST",
            {"text": "歩いてみる"},
        )
        assert status == 200
        assert turn["status"] == "completed"
        assert turn["transition_kind"] == "thread.turn_added"

        status, state = request_json("http://127.0.0.1:8000/sessions/dogfight-http-pipeline/state")
        assert status == 200
        assert state["landscape"]["scene_id"] == scene["scene_id"]
        assert state["landscape"]["text"] == "歩いてみる"
        assert state["turn_count"] == 1
        assert state["context"]["source_ids"] == ["dogfight_scene"]

        status, evidence = request_json("http://127.0.0.1:8000/sessions/dogfight-http-pipeline/evidence")
        assert status == 200
        assert len(evidence) == 1
        assert evidence[0]["status"] == "completed"
        assert evidence[0]["transition_kind"] == "thread.turn_added"
    finally:
        process.terminate()
        process.wait(timeout=5)
