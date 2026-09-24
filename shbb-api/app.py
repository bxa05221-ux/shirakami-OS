"""HTTP API boundary for the Shirakami Runtime β1.0 observation path."""

from hashlib import sha256
from typing import Any, Literal

from pydantic import BaseModel, Field

from runtime.api_semantic_handoff import preserve_protocol_reference, validate_semantic_handoff
from runtime.landscape import LandscapeState
from runtime.semantic_handoff import SemanticHandoff


class ObservationProvenance(BaseModel):
    """Runtime provenance returned by the observation boundary."""

    runtime: str
    transition: bool


class ObserveResponse(BaseModel):
    """Concrete implementation invariant for a successful observation."""

    landscape_id: str
    observation_id: str = Field(pattern=r"^[0-9a-f]{16}$")
    state: Literal["observed"]
    evidence_id: str | None
    protocol_id: str | None
    result: dict[str, Any]
    provenance: ObservationProvenance


def observe(payload: dict[str, Any]) -> dict[str, Any]:
    """Execute the minimal observation boundary without inventing a transition."""
    validate_semantic_handoff(payload)

    landscape_id = payload.get("landscape_id")
    input_value = payload.get("input")
    if not isinstance(landscape_id, str) or not landscape_id:
        raise ValueError("landscape_id is required")
    if not isinstance(input_value, dict):
        raise ValueError("input must be an object")

    state = LandscapeState.from_snapshot(input_value)
    snapshot = dict(state.snapshot())
    observation_id = sha256(
        (landscape_id + "\\n" + repr(sorted(snapshot.items()))).encode("utf-8")
    ).hexdigest()[:16]

    response = {
        "landscape_id": landscape_id,
        "observation_id": observation_id,
        "state": "observed",
        "evidence_id": None,
        "protocol_id": preserve_protocol_reference(payload),
        "result": snapshot,
        "provenance": {"runtime": "LandscapeState.from_snapshot", "transition": False},
    }
    return ObserveResponse.model_validate(response).model_dump()


def semantic_handoff(payload: dict[str, Any]) -> dict[str, Any]:
    """Create a deterministic semantic handoff without inferring authority."""
    evidence_ids = payload.get("evidence_ids", [])
    if not isinstance(evidence_ids, list) or not all(isinstance(item, str) and item for item in evidence_ids):
        raise ValueError("evidence_ids must be an array of non-empty strings")
    interpretation_id = payload.get("interpretation_id")
    decision_id = payload.get("decision_id")
    gate_id = payload.get("gate_id")
    for name, value in (("interpretation_id", interpretation_id), ("decision_id", decision_id), ("gate_id", gate_id)):
        if value is not None and (not isinstance(value, str) or not value):
            raise ValueError(f"{name} must be a non-empty string when supplied")
    body = payload.get("payload", {})
    if not isinstance(body, dict):
        raise ValueError("payload must be an object")
    handoff = SemanticHandoff(
        evidence_ids=tuple(evidence_ids),
        interpretation_id=interpretation_id,
        decision_id=decision_id,
        gate_id=gate_id,
        payload=body,
    )
    return {
        "handoff_id": handoff.handoff_id,
        "evidence_ids": list(handoff.evidence_ids),
        "interpretation_id": handoff.interpretation_id,
        "decision_id": handoff.decision_id,
        "gate_id": handoff.gate_id,
        "payload": dict(handoff.payload),
        "authority": "not_inferred",
    }


def create_app():
    """Create the public Shirakami API application."""
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.exceptions import RequestValidationError
    from fastapi.responses import JSONResponse

    app = FastAPI(title="Shirakami API", version="0.1.0")

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": "request body must be an object"})

    @app.post("/observe")
    def observe_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return observe(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/handoff")
    def semantic_handoff_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return semantic_handoff(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    return app
