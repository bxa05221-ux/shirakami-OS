from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / "tests" / "fixtures" / "dogfight_scene.json"


def _request(method: str, url: str, payload: dict | None = None) -> tuple[int, dict | list]:
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(url, data=body, method=method)
    if body is not None:
        request.add_header("Content-Type", "application/json; charset=utf-8")
    with urlopen(request, timeout=5) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def test_real_landscape_round_trip_over_http() -> None:
    scene = json.loads(SCENE.read_text(encoding="utf-8"))
    process = subprocess.Popen(
        [sys.executable, "-m", "runtime.http_api"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        base = "http://127.0.0.1:8000"
        for _ in range(30):
            try:
                urlopen(base, timeout=0.2).close()
                break
            except Exception:
                time.sleep(0.1)
        else:
            raise AssertionError("HTTP API did not start")

        status, created = _request(
            "POST",
            f"{base}/sessions",
            {
                "session_id": "dogfight-http",
                "landscape_ref": "dogfight_scene.json",
                "landscape": scene,
            },
        )
        assert status == 201
        assert created["landscape"]["scene_id"] == scene["scene_id"]

        status, turn = _request(
            "POST",
            f"{base}/sessions/dogfight-http/turns",
            {"text": "歩いてみる"},
        )
        assert status == 200
        assert turn["status"] == "completed"
        assert turn["transition_kind"] == "thread.turn_added"
        assert turn["state"]["landscape"]["text"] == "歩いてみる"
        assert turn["state"]["landscape"]["scene_id"] == scene["scene_id"]

        status, state = _request("GET", f"{base}/sessions/dogfight-http/state")
        assert status == 200
        assert state["turn_count"] == 1
        assert state["landscape"]["scene_id"] == scene["scene_id"]
        assert state["landscape"]["text"] == "歩いてみる"

        status, evidence = _request("GET", f"{base}/sessions/dogfight-http/evidence")
        assert status == 200
        assert len(evidence) == 1
        assert evidence[0]["status"] == "completed"
        assert evidence[0]["transition_kind"] == "thread.turn_added"
        assert evidence[0]["transition_data"]["text"] == "歩いてみる"
    finally:
        process.terminate()
        process.wait(timeout=5)
