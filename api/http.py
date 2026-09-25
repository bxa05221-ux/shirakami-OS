"""HTTP transport for the provider-neutral UI for AI API alpha 0.1."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Callable, Mapping

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

try:
    from ..runtime.api import ShirakamiAPI
    from ..runtime.evolution_bridge import ContextSnapshot
    from .auth import require_api_key
    from .boundary import validate_execution_context
except ImportError:
    from runtime.api import ShirakamiAPI
    from runtime.evolution_bridge import ContextSnapshot
    from api.auth import require_api_key
    from api.boundary import validate_execution_context


class ContextSnapshotInput(BaseModel):
    protocol_id: str
    landscape: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ObserveInput(BaseModel):
    observation: dict[str, Any] = Field(default_factory=dict)
    context: ContextSnapshotInput
    handoff_id: str
    trace_id: str | None = None
    evidence_ids: list[str] = Field(default_factory=list)


class AnalyzeInput(BaseModel):
    protocol_id: str
    protocol_exists: bool = True
    diff_ref: str = ""


class ApproveInput(BaseModel):
    approved: bool = True
    reviewer: str = "human"
    human_authorized: bool = False


class ExecutionBoundaryContext(BaseModel):
    handoff_id: str
    project: str
    objective: str
    protocol_ids: list[str]
    evidence_ids: list[str] = Field(default_factory=list)
    verification_scope: list[Any] = Field(default_factory=list)
    execution_authorized: bool = False
    publish_authorized: bool = False
    merge_authorized: bool = False
    human_gate_required: bool = True


class ExecuteInput(BaseModel):
    protocol_id: str
    input_data: dict[str, Any] = Field(default_factory=dict)
    handoff_id: str
    trace_id: str | None = None
    evidence_ids: list[str] = Field(default_factory=list)
    boundary_context: ExecutionBoundaryContext


class VerifyInput(BaseModel):
    execution: dict[str, Any] = Field(default_factory=dict)
    expected_transition_kind: str | None = None
    diff_ref: str = ""


class ShirakamiHTTPTransport:
    """Build a transport adapter without coupling Runtime to HTTP."""

    def __init__(self, api: ShirakamiAPI | None = None, protocol_registry: Mapping[str, Callable[[Any], Any]] | None = None, api_key: str | None = None) -> None:
        self.api = api or ShirakamiAPI()
        self.protocol_registry = dict(protocol_registry or {})
        self.api_key = api_key

    def create_app(self) -> FastAPI:
        app = FastAPI(title="Shirakami UI for AI API", version="alpha-0.1")
        auth = require_api_key(self.api_key)

        @app.get("/health")
        def health() -> dict[str, str]:
            return {"status": "ok"}

        @app.post("/v1/observe", dependencies=[Depends(auth)])
        def observe(payload: ObserveInput) -> dict[str, Any]:
            context = ContextSnapshot(protocol_id=payload.context.protocol_id, landscape=payload.context.landscape, metadata=payload.context.metadata)
            result = self.api.observe(payload.observation, context)
            result.update({"handoff_id": payload.handoff_id, "trace_id": payload.trace_id, "evidence_ids": list(payload.evidence_ids), "execution_authorized": False, "publish_authorized": False, "merge_authorized": False, "human_gate_required": True})
            return result

        @app.post("/v1/analyze", dependencies=[Depends(auth)])
        def analyze(payload: AnalyzeInput) -> dict[str, Any]:
            return asdict(self.api.analyze(payload.protocol_id, protocol_exists=payload.protocol_exists, diff_ref=payload.diff_ref))

        @app.post("/v1/approve", dependencies=[Depends(auth)])
        def approve(payload: ApproveInput) -> dict[str, Any]:
            return self.api.approve(approved=payload.approved, reviewer=payload.reviewer, human_authorized=payload.human_authorized)

        @app.post("/v1/execute", dependencies=[Depends(auth)])
        def execute(payload: ExecuteInput) -> dict[str, Any]:
            boundary = validate_execution_context(payload.boundary_context.model_dump())
            if boundary["handoff_id"] != payload.handoff_id or boundary["evidence_ids"] != payload.evidence_ids:
                raise HTTPException(status_code=422, detail="transport and boundary context mismatch")
            if payload.protocol_id not in boundary["protocol_ids"]:
                raise HTTPException(status_code=422, detail="protocol_id is not declared by boundary context")
            protocol = self.protocol_registry.get(payload.protocol_id)
            if protocol is None:
                raise HTTPException(status_code=404, detail="protocol is not registered for HTTP execution")
            return self.api.execute(protocol, payload.protocol_id, payload.input_data, handoff_id=payload.handoff_id, trace_id=payload.trace_id, evidence_ids=tuple(payload.evidence_ids), project=boundary["project"], objective=boundary["objective"], protocol_ids=tuple(boundary["protocol_ids"]), verification_scope=tuple(boundary["verification_scope"]))

        @app.get("/v1/executions/{execution_id}", dependencies=[Depends(auth)])
        def get_execution(execution_id: str) -> dict[str, Any]:
            result = self.api.get_execution(execution_id)
            if result is None:
                raise HTTPException(status_code=404, detail="unknown execution_id")
            return result

        @app.get("/v1/traces/{trace_id}", dependencies=[Depends(auth)])
        def get_trace(trace_id: str) -> dict[str, Any]:
            result = self.api.get_trace(trace_id)
            if result is None:
                raise HTTPException(status_code=404, detail="unknown trace_id")
            return result

        @app.get("/v1/witnesses/{trace_id}/history", dependencies=[Depends(auth)])
        def get_witness_history(trace_id: str) -> list[dict[str, Any]]:
            return self.api.get_witness_history(trace_id)

        @app.get("/v1/witnesses/{trace_id}", dependencies=[Depends(auth)])
        def get_witness(trace_id: str) -> dict[str, Any]:
            result = self.api.get_witness(trace_id)
            if result is None:
                raise HTTPException(status_code=404, detail="unknown trace_id")
            return result

        @app.get("/v1/traceability/{trace_id}", dependencies=[Depends(auth)])
        def get_traceability(trace_id: str) -> dict[str, Any]:
            trace = self.api.get_trace(trace_id)
            witness = self.api.get_witness(trace_id)
            if trace is None or witness is None:
                raise HTTPException(status_code=404, detail="unknown trace_id")
            execution_id = trace.get("execution_id")
            execution = self.api.get_execution(execution_id) if execution_id else None
            if execution is None:
                raise HTTPException(status_code=404, detail="execution for trace is unavailable")
            from aiwitness.traceability import validate_traceability
            try:
                record = validate_traceability(trace=trace, witness=witness, execution=execution, evidence_ids=trace.get("evidence_ids", []))
            except ValueError as exc:
                raise HTTPException(status_code=409, detail=str(exc)) from exc
            return {"valid": True, "traceability": asdict(record)}

        @app.post("/v1/executions/{execution_id}/verify", dependencies=[Depends(auth)])
        def verify_execution(execution_id: str, payload: VerifyInput) -> dict[str, Any]:
            result = self.api.verify_execution(execution_id, expected_transition_kind=payload.expected_transition_kind, diff_ref=payload.diff_ref)
            if result is None:
                raise HTTPException(status_code=404, detail="unknown execution_id")
            return asdict(result)

        @app.get("/v1/evidence", dependencies=[Depends(auth)])
        def evidence(protocol_id: str | None = None, signal: str | None = None, transition_kind: str | None = None) -> list[dict[str, Any]]:
            return list(self.api.query_evidence(protocol_id=protocol_id, signal=signal, transition_kind=transition_kind))

        @app.get("/v1/evidence/{evidence_id}", dependencies=[Depends(auth)])
        def evidence_by_id(evidence_id: str) -> dict[str, Any]:
            result = self.api.get_evidence(evidence_id)
            if result is None:
                raise HTTPException(status_code=404, detail="unknown evidence_id")
            return result

        return app


def create_app(api: ShirakamiAPI | None = None, protocol_registry: Mapping[str, Callable[[Any], Any]] | None = None, api_key: str | None = None) -> FastAPI:
    return ShirakamiHTTPTransport(api, protocol_registry, api_key).create_app()
