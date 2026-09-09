"""HTTP API boundary for the Shirakami Runtime β1.0 observation path."""

from hashlib import sha256
from typing import Any

from runtime.landscape import LandscapeState


def observe(payload: dict[str, Any]) -> dict[str, Any]:
    """Execute the minimal observation boundary without inventing a transition."""
    landscape_id = payload.get("landscape_id")
    input_value = payload.get("input")
    if not isinstance(landscape_id, str) or not landscape_id:
        raise ValueError("landscape_id is required")
    if not isinstance(input_value, dict):
        raise ValueError("input must be an object")

    state = LandscapeState.from_snapshot(input_value)
    snapshot = dict(state.snapshot())
    observation_id = sha256(
        (landscape_id + "\n" + repr(sorted(snapshot.items()))).encode("utf-8")
    ).hexdigest()[:16]

    return {
        "landscape_id": landscape_id,
        "observation_id": observation_id,
        "state": "observed",
        "evidence_id": None,
        "protocol_id": payload.get("protocol_id"),
        "result": snapshot,
        "provenance": {"runtime": "LandscapeState.from_snapshot", "transition": False},
    }


def create_app():
    """Create the public Shirakami API application."""
    from fastapi import FastAPI, HTTPException

    app = FastAPI(title="Shirakami API", version="0.1.0")

    @app.post("/observe")
    def observe_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return observe(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    return app
