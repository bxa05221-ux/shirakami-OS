"""Minimal HTTP-facing API for the Shirakami Runtime alpha 0.1."""

from typing import Any

from plugins.adapters.github.github_adapter import GitHubAdapter
from runtime.evidence import EvidenceRecord
from runtime.interpretation import InterpretationRecord
from runtime.oppai_schema import normalize as normalize_oppai, to_dict as oppai_to_dict
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


def _evidence_to_dict(record: EvidenceRecord) -> dict[str, Any]:
    """Serialize the canonical EvidenceRecord without changing its identity."""
    return {
        "evidence_id": record.evidence_id,
        "protocol_id": record.protocol_id,
        "status": record.status,
        "transition_kind": record.transition_kind,
        "transition_data": dict(record.transition_data),
        "signals": list(record.signals),
        "confidence": record.confidence,
    }


def _interpretation_to_dict(record: InterpretationRecord) -> dict[str, Any]:
    """Serialize the canonical InterpretationRecord without changing identity."""
    return {
        "interpretation_id": record.interpretation_id,
        "source_evidence": list(record.source_evidence),
        "actor_id": record.actor_id,
        "content": dict(record.content),
        "status": record.status,
    }


def create_app():
    """Create a FastAPI app when FastAPI is installed."""
    from fastapi import FastAPI, HTTPException

    app = FastAPI(title="Shirakami Runtime API", version="0.1.0")
    evidence_registry: dict[str, EvidenceRecord] = {}
    interpretation_registry: dict[str, InterpretationRecord] = {}

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": "0.1.0"}

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

    @app.post("/v0.1/evidence", status_code=201)
    def evidence_create_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        required = ("protocol_id", "status", "transition_kind", "transition_data", "signals")
        if any(key not in payload for key in required):
            raise HTTPException(status_code=400, detail="protocol_id, status, transition_kind, transition_data and signals are required")
        if not isinstance(payload["transition_data"], dict) or not isinstance(payload["signals"], list):
            raise HTTPException(status_code=400, detail="transition_data must be an object and signals must be an array")
        record = EvidenceRecord(
            protocol_id=payload["protocol_id"],
            status=payload["status"],
            transition_kind=payload["transition_kind"],
            transition_data=payload["transition_data"],
            signals=tuple(payload["signals"]),
            confidence=payload.get("confidence", "observed"),
        )
        existing = evidence_registry.get(record.evidence_id)
        if existing is not None and existing != record:
            raise HTTPException(status_code=409, detail="evidence_id collision")
        evidence_registry[record.evidence_id] = record
        return _evidence_to_dict(record)

    @app.get("/v0.1/evidence/{evidence_id}")
    def evidence_get_endpoint(evidence_id: str) -> dict[str, Any]:
        record = evidence_registry.get(evidence_id)
        if record is None:
            raise HTTPException(status_code=404, detail="evidence not found")
        return _evidence_to_dict(record)

    @app.post("/v0.1/interpretations", status_code=201)
    def interpretation_create_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        required = ("source_evidence", "actor_id", "content")
        if any(key not in payload for key in required):
            raise HTTPException(status_code=400, detail="source_evidence, actor_id and content are required")
        if not isinstance(payload["source_evidence"], list) or not all(isinstance(item, str) for item in payload["source_evidence"]):
            raise HTTPException(status_code=400, detail="source_evidence must be an array of strings")
        if not isinstance(payload["actor_id"], str) or not isinstance(payload["content"], dict):
            raise HTTPException(status_code=400, detail="actor_id must be a string and content must be an object")
        missing = [evidence_id for evidence_id in payload["source_evidence"] if evidence_id not in evidence_registry]
        if missing:
            raise HTTPException(status_code=404, detail={"missing_evidence": missing})
        record = InterpretationRecord(
            source_evidence=tuple(payload["source_evidence"]),
            actor_id=payload["actor_id"],
            content=payload["content"],
            status=payload.get("status", "proposed"),
        )
        existing = interpretation_registry.get(record.interpretation_id)
        if existing is not None and existing != record:
            raise HTTPException(status_code=409, detail="interpretation_id collision")
        interpretation_registry[record.interpretation_id] = record
        return _interpretation_to_dict(record)

    @app.get("/v0.1/interpretations/{interpretation_id}")
    def interpretation_get_endpoint(interpretation_id: str) -> dict[str, Any]:
        record = interpretation_registry.get(interpretation_id)
        if record is None:
            raise HTTPException(status_code=404, detail="interpretation not found")
        return _interpretation_to_dict(record)

    return app
