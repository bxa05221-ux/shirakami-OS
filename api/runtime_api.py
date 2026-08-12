"""Minimal HTTP-facing API for the Shirakami Runtime alpha 0.1.

The API exposes the existing Protocol -> Runtime vertical slice without
introducing authentication, persistence, scheduling, or a new runtime core.
"""

from typing import Any

from runtime.protocol_runtime_bridge import execute_protocol


def execute(payload: dict[str, Any]) -> dict[str, Any]:
    """Execute one supported Protocol IR transition.

    Request shape:
        {
            "protocol": {"matome": {"title": ..., "version": ...}},
            "input": ...
        }

    The transition is deliberately limited to an echo operation in alpha
    0.1. This makes the API boundary testable without inventing new protocol
    semantics.
    """
    protocol = payload.get("protocol")
    if not isinstance(protocol, dict):
        raise ValueError("protocol must be an object")

    operation = payload.get("operation", "echo")
    if operation != "echo":
        raise ValueError("unsupported operation")

    execution = execute_protocol(
        protocol,
        lambda value: value,
        input_value=payload.get("input"),
    )

    result = execution.result
    return {
        "protocol": {
            "title": execution.protocol_title,
            "version": execution.protocol_version,
        },
        "success": result.success,
        "event": result.event,
        "output": result.output,
        "error": result.error,
    }


def create_app():
    """Create a FastAPI app when FastAPI is installed."""
    from fastapi import FastAPI, HTTPException

    app = FastAPI(title="Shirakami Runtime API", version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": "0.1.0"}

    @app.post("/v0.1/execute")
    def execute_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return execute(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    return app
