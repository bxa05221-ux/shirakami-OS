"""Minimal HTTP-facing API for the Shirakami Runtime alpha 0.1."""

from typing import Any

from plugins.adapters.github.github_adapter import GitHubAdapter
from runtime.protocol_runtime_bridge import execute_protocol
from runtime.prototype import Transition


def execute(payload: dict[str, Any]) -> dict[str, Any]:
    """Execute one supported Protocol IR transition."""
    protocol = payload.get("protocol")
    if not isinstance(protocol, dict):
        raise ValueError("protocol must be an object")
    if payload.get("operation", "echo") != "echo":
        raise ValueError("unsupported operation")

    def echo_transition(value: Any) -> Transition:
        return Transition(kind="api.echo", data={"output": value})

    execution = execute_protocol(
        protocol,
        echo_transition,
        input_value=payload.get("input"),
    )
    result = execution.result
    completed = result.status == "completed"
    return {
        "protocol": {"title": execution.protocol_title, "version": execution.protocol_version},
        "success": completed,
        "event": "execution.completed" if completed else "execution.failed",
        "output": result.transition.data.get("output"),
        "error": None if completed else result.transition.data,
    }


def observe(payload: dict[str, Any]) -> dict[str, Any]:
    """Record an observation/proposal without promoting it to state."""
    observation = payload.get("observation")
    if observation is None:
        raise ValueError("observation is required")
    return {
        "status": "observed",
        "state_transition": False,
        "observation": observation,
    }


def evidence(evidence_id: str) -> dict[str, Any]:
    """Return a placeholder lookup boundary for immutable evidence."""
    if not evidence_id:
        raise ValueError("evidence_id is required")
    return {"evidence_id": evidence_id, "status": "lookup_boundary"}


def github_read(payload: dict[str, Any], adapter: GitHubAdapter | None = None) -> dict[str, Any]:
    """Observe a GitHub file through the Adapter boundary."""
    repository, path = payload.get("repository"), payload.get("path")
    if not isinstance(repository, str) or not isinstance(path, str):
        raise ValueError("repository and path are required")
    file = (adapter or GitHubAdapter()).read_file(repository, path, payload.get("ref", "main"))
    return {"repository": file.repository, "path": file.path, "sha": file.sha,
            "content": file.content, "event": "backend.observed"}


def github_controlled_write(payload: dict[str, Any], adapter: GitHubAdapter | None = None) -> dict[str, Any]:
    """Perform a controlled write followed immediately by Adapter read-back."""
    required = ("repository", "path", "content", "message", "sha")
    if any(not isinstance(payload.get(key), str) for key in required):
        raise ValueError("repository, path, content, message and sha are required")
    github = adapter or GitHubAdapter()
    result = github.write_file(
        payload["repository"], payload["path"], payload["content"],
        payload["message"], payload["sha"], payload.get("branch", "main"),
    )
    return {
        "repository": result.repository, "path": result.path,
        "sha": result.sha, "content": result.content,
        "event": "backend.write.readback",
        "evidence": {"operation": "controlled_write", "read_back": True},
    }


def create_app():
    """Create a FastAPI app when FastAPI is installed."""
    from fastapi import FastAPI, HTTPException

    app = FastAPI(title="Shirakami Runtime API", version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": "0.1.0"}

    @app.post("/v1/execute")
    @app.post("/v0.1/execute")
    def execute_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return execute(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/v1/observe")
    @app.post("/v0.1/observe")
    def observe_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return observe(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/v1/evidence/{evidence_id}")
    @app.get("/v0.1/evidence/{evidence_id}")
    def evidence_endpoint(evidence_id: str) -> dict[str, Any]:
        try:
            return evidence(evidence_id)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/v1/github/read")
    @app.post("/v0.1/github/read")
    def github_read_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return github_read(payload)
        except (ValueError, RuntimeError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/v1/github/write")
    @app.post("/v0.1/github/write")
    def github_write_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return github_controlled_write(payload)
        except (PermissionError, ValueError, RuntimeError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    return app
