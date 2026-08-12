"""Minimal HTTP-facing API for the Shirakami Runtime alpha 0.1.

The API exposes the existing Protocol -> Runtime vertical slice and a thin
GitHub Adapter boundary for controlled observation/write-back experiments.
"""

from typing import Any

from plugins.adapters.github.github_adapter import GitHubAdapter
from runtime.protocol_runtime_bridge import execute_protocol


def execute(payload: dict[str, Any]) -> dict[str, Any]:
    """Execute one supported Protocol IR transition."""
    protocol = payload.get("protocol")
    if not isinstance(protocol, dict):
        raise ValueError("protocol must be an object")
    if payload.get("operation", "echo") != "echo":
        raise ValueError("unsupported operation")

    execution = execute_protocol(
        protocol,
        lambda value: value,
        input_value=payload.get("input"),
    )
    result = execution.result
    return {
        "protocol": {"title": execution.protocol_title, "version": execution.protocol_version},
        "success": result.success,
        "event": result.event,
        "output": result.output,
        "error": result.error,
    }


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

    @app.post("/v0.1/execute")
    def execute_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return execute(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/v0.1/github/read")
    def github_read_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return github_read(payload)
        except (ValueError, RuntimeError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/v0.1/github/write")
    def github_write_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return github_controlled_write(payload)
        except (PermissionError, ValueError, RuntimeError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    return app
