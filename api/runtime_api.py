"""HTTP-facing API for the Shirakami Runtime.

The α0.1 endpoints remain available for compatibility. The β1.0 endpoints
expose the smallest usable application-facing flow:

Client -> Public API -> Shirakami OS -> Landscape/Evidence

Backend-specific transport remains outside the β1.0 core flow.
"""

from typing import Any

from plugins.adapters.github.github_adapter import GitHubAdapter
from runtime.evidence import capture_evidence
from runtime.oppai_schema import normalize as normalize_oppai, to_dict as oppai_to_dict
from runtime.prototype import ExecutionContext, Transition
from shirakami_os import ShirakamiOS


def execute(payload: dict[str, Any]) -> dict[str, Any]:
    """Execute one supported Protocol IR transition (α0.1 compatibility)."""
    protocol = payload.get("protocol")
    if not isinstance(protocol, dict):
        raise ValueError("protocol must be an object")
    if payload.get("operation", "echo") != "echo":
        raise ValueError("unsupported operation")

    from runtime.protocol_runtime_bridge import execute_protocol

    def echo_transition(value: Any) -> Transition:
        return Transition(kind="api.echo", data={"output": value})

    execution = execute_protocol(protocol, echo_transition, input_value=payload.get("input"))
    result = execution.result
    return {
        "protocol": {"title": execution.protocol_title, "version": execution.protocol_version},
        "success": result.status == "completed",
        "event": result.signals[0] if result.signals else None,
        "output": result.transition.data.get("output"),
        "error": None if result.status == "completed" else result.transition.data,
    }


def oppai_normalize(payload: dict[str, Any]) -> dict[str, Any]:
    """Run the dependency-light OPPAI preprocessing boundary."""
    text = payload.get("text")
    if not isinstance(text, str):
        raise ValueError("text is required")
    observation = normalize_oppai(text, payload.get("context"))
    return {"schema": "OPPAI", "version": "0.1", "event": "oppai.observed", **oppai_to_dict(observation)}


def github_read(payload: dict[str, Any], adapter: GitHubAdapter | None = None) -> dict[str, Any]:
    """Observe a GitHub file through the Adapter boundary (α0.1 compatibility)."""
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


class Beta1ReferenceRuntime:
    """Small application-facing state holder for the β1.0 reference flow.

    This intentionally uses the existing ShirakamiOS boundary rather than
    introducing a second Runtime implementation. State is in-memory for the
    reference implementation; persistence is outside β1.0 scope.
    """

    def __init__(self) -> None:
        self.os = ShirakamiOS()
        self.evidence: list[dict[str, Any]] = []
        self.os.boot()

    @staticmethod
    def _echo_protocol(context: ExecutionContext) -> Transition:
        return Transition(
            kind="landscape.message.received",
            data={"changed": True, "message": context.input.get("message", "")},
        )

    def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        protocol = payload.get("protocol")
        if not isinstance(protocol, dict):
            raise ValueError("protocol must be an object")
        operation = payload.get("operation", "message")
        if operation != "message":
            raise ValueError("unsupported β1.0 reference operation")

        matome = protocol.get("matome", protocol)
        if not isinstance(matome, dict):
            raise ValueError("protocol IR must contain an object-like matome")
        protocol_id = str(matome.get("title") or "anonymous.protocol")
        result = self.os.execute(protocol_id, self._echo_protocol, payload.get("input", {}))
        evidence = {
            "protocol_id": result.protocol_id,
            "status": result.status,
            "transition": result.transition.kind,
            "transition_data": dict(result.evidence.transition_data),
        }
        self.evidence.append(evidence)
        return {
            "protocol": {"id": result.protocol_id, "version": str(matome.get("version", ""))},
            "status": result.status,
            "transition": {"kind": result.transition.kind, "data": dict(result.transition.data)},
            "evidence": evidence,
            "landscape": dict(result.landscape),
        }

    def observe_landscape(self) -> dict[str, Any]:
        return {"landscape": dict(self.os.landscape.snapshot())}

    def observe_evidence(self) -> dict[str, Any]:
        return {"evidence": list(self.evidence)}


_BETA1 = Beta1ReferenceRuntime()


def create_app():
    """Create a FastAPI app when FastAPI is installed."""
    from fastapi import FastAPI, HTTPException

    app = FastAPI(title="Shirakami Runtime API", version="1.0.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": "1.0.0"}

    @app.post("/v0.1/execute")
    def execute_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return execute(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/v0.1/oppai/normalize")
    def oppai_normalize_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return oppai_normalize(payload)
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

    # β1.0 application-facing boundary.
    @app.post("/v1/execute")
    def beta1_execute_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return _BETA1.execute(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/v1/landscape/observe")
    def beta1_landscape_endpoint() -> dict[str, Any]:
        return _BETA1.observe_landscape()

    @app.post("/v1/evidence/observe")
    def beta1_evidence_endpoint() -> dict[str, Any]:
        return _BETA1.observe_evidence()

    @app.post("/v1/adapter/invoke")
    def beta1_adapter_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        raise HTTPException(
            status_code=501,
            detail="adapter invocation is reserved for an explicit Adapter implementation",
        )

    return app
