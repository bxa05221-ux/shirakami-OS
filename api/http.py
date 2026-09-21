"""HTTP transport for the provider-neutral UI for AI API alpha 0.1.

The semantic boundary remains in :mod:`runtime.api`.  This module only
translates JSON/HTTP requests into semantic API calls and back.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Callable, Mapping

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

try:
    from ..runtime.api import ShirakamiAPI
    from ..runtime.evolution_bridge import ContextSnapshot
except ImportError:
    from runtime.api import ShirakamiAPI
    from runtime.evolution_bridge import ContextSnapshot


class ContextSnapshotInput(BaseModel):
    protocol_id: str
    landscape: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ObserveInput(BaseModel):
    observation: dict[str, Any] = Field(default_factory=dict)
    context: ContextSnapshotInput


class AnalyzeInput(BaseModel):
    protocol_id: str
    protocol_exists: bool = True
    diff_ref: str = ""


class ApproveInput(BaseModel):
    approved: bool = True
    reviewer: str = "human"
    human_authorized: bool = False


class ExecuteInput(BaseModel):
    protocol_id: str
    input_data: dict[str, Any] = Field(default_factory=dict)


class VerifyInput(BaseModel):
    # Optional for handle-based verification: the execution is resolved by path.
    # Retained for the legacy semantic verification boundary.
    execution: dict[str, Any] = Field(default_factory=dict)
    expected_transition_kind: str | None = None
    diff_ref: str = ""


class ShirakamiHTTPTransport:
    """Build a transport adapter without coupling Runtime to HTTP."""

    def __init__(
        self,
        api: ShirakamiAPI | None = None,
        protocol_registry: Mapping[str, Callable[[Any], Any]] | None = None,
    ) -> None:
        self.api = api or ShirakamiAPI()
        self.protocol_registry = dict(protocol_registry or {})

    def create_app(self) -> FastAPI:
        app = FastAPI(
            title="Shirakami UI for AI API",
            version="alpha-0.1",
            description=(
                "Bidirectional transport boundary between external UI systems "
                "and the Shirakami Evidence-driven Runtime."
            ),
        )

        @app.get("/health")
        def health() -> dict[str, str]:
            return {"status": "ok"}

        @app.post("/v1/observe")
        def observe(payload: ObserveInput) -> dict[str, Any]:
            context = ContextSnapshot(
                protocol_id=payload.context.protocol_id,
                landscape=payload.context.landscape,
                metadata=payload.context.metadata,
            )
            return self.api.observe(payload.observation, context)

        @app.post("/v1/analyze")
        def analyze(payload: AnalyzeInput) -> dict[str, Any]:
            result = self.api.analyze(
                payload.protocol_id,
                protocol_exists=payload.protocol_exists,
                diff_ref=payload.diff_ref,
            )
            return asdict(result)

        @app.post("/v1/approve")
        def approve(payload: ApproveInput) -> dict[str, Any]:
            return self.api.approve(
                approved=payload.approved,
                reviewer=payload.reviewer,
                human_authorized=payload.human_authorized,
            )

        @app.post("/v1/execute")
        def execute(payload: ExecuteInput) -> dict[str, Any]:
            protocol = self.protocol_registry.get(payload.protocol_id)
            if protocol is None:
                raise HTTPException(
                    status_code=404,
                    detail="protocol is not registered for HTTP execution",
                )
            return self.api.execute(
                protocol,
                payload.protocol_id,
                payload.input_data,
            )

        @app.get("/v1/executions/{execution_id}")
        def get_execution(execution_id: str) -> dict[str, Any]:
            result = self.api.get_execution(execution_id)
            if result is None:
                raise HTTPException(status_code=404, detail="unknown execution_id")
            return result

        @app.post("/v1/executions/{execution_id}/verify")
        def verify_execution(execution_id: str, payload: VerifyInput) -> dict[str, Any]:
            result = self.api.verify_execution(
                execution_id,
                expected_transition_kind=payload.expected_transition_kind,
                diff_ref=payload.diff_ref,
            )
            if result is None:
                raise HTTPException(status_code=404, detail="unknown execution_id")
            return asdict(result)

        @app.post("/v1/verify")
        def verify(payload: VerifyInput) -> dict[str, Any]:
            raise HTTPException(
                status_code=400,
                detail="use /v1/executions/{execution_id}/verify; execution_id is required",
            )

        @app.get("/v1/evidence")
        def evidence(
            protocol_id: str | None = None,
            signal: str | None = None,
            transition_kind: str | None = None,
        ) -> list[dict[str, Any]]:
            return list(
                self.api.query_evidence(
                    protocol_id=protocol_id,
                    signal=signal,
                    transition_kind=transition_kind,
                )
            )

        return app


def create_app(
    api: ShirakamiAPI | None = None,
    protocol_registry: Mapping[str, Callable[[Any], Any]] | None = None,
) -> FastAPI:
    """Convenience factory for WSGI/ASGI hosts and tests."""
    return ShirakamiHTTPTransport(api, protocol_registry).create_app()
