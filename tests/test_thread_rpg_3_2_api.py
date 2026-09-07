"""HTTP boundary tests for Thread RPG 3.2."""

import pytest

fastapi = pytest.importorskip("fastapi")
httpx = pytest.importorskip("httpx")

from fastapi.testclient import TestClient

from api.thread_rpg_api import create_app


def test_thread_rpg_http_vertical_slice():
    client = TestClient(create_app())

    created = client.post("/sessions", json={"landscape_ref": "landscape:test"})
    assert created.status_code == 200
    session_id = created.json()["session_id"]

    turn = client.post(
        f"/sessions/{session_id}/turns",
        json={"participant_input": "旅を続けよう"},
    )
    assert turn.status_code == 200
    assert turn.json()["evidence"]["transition_kind"] == "thread.turn_added"

    state = client.get(f"/sessions/{session_id}/state")
    assert state.status_code == 200
    assert len(state.json()["turns"]) == 1

    evidence = client.get(f"/sessions/{session_id}/evidence")
    assert evidence.status_code == 200
    assert len(evidence.json()) == 1
