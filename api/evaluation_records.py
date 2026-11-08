"""Isolated evaluation record API reference. Never mount without trusted provisioning.

In-memory identity, keys and records: synthetic test data only, not production.
No LLM adapter or outbound transport is exposed by this application.
"""
from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from security.evaluator_identity import EvaluatorAuthDenied, EvaluatorIdentityRegistry
from security.local_store import AccessDenied, EncryptedEvaluationStore


class PrivateRecordInput(BaseModel):
    record_id: str = Field(min_length=1)
    content: str


class ConsensusInput(BaseModel):
    recipients: set[str] = Field(min_length=1)


def create_evaluation_records_app(
    identities: EvaluatorIdentityRegistry,
    store: EncryptedEvaluationStore,
) -> FastAPI:
    """Explicit trusted dependencies; no HTTP provisioning endpoint."""
    app = FastAPI(title="Evaluation Records Reference API", version="p0-reference")

    def principal_for(project_id: str, token: str | None):
        try:
            return identities.authenticate(token, project_id)
        except EvaluatorAuthDenied:
            raise HTTPException(status_code=403, detail="evaluator access denied") from None

    @app.post("/evaluation/projects/{project_id}/records", status_code=201)
    def create_record(project_id: str, payload: PrivateRecordInput, x_evaluator_token: str | None = Header(default=None)):
        principal = principal_for(project_id, x_evaluator_token)
        try:
            store.put_private(payload.record_id, project_id, principal.evaluator_id, payload.content.encode("utf-8"))
        except AccessDenied:
            raise HTTPException(status_code=403, detail="record access denied") from None
        return {"record_id": payload.record_id, "project_id": project_id, "owner_id": principal.evaluator_id}

    @app.get("/evaluation/projects/{project_id}/records/{record_id}")
    def read_record(project_id: str, record_id: str, x_evaluator_token: str | None = Header(default=None)):
        principal = principal_for(project_id, x_evaluator_token)
        try:
            content = store.read(record_id, project_id, principal.evaluator_id)
        except AccessDenied:
            raise HTTPException(status_code=403, detail="record access denied") from None
        return {"record_id": record_id, "content": content.decode("utf-8")}

    @app.post("/evaluation/projects/{project_id}/records/{record_id}/share")
    def share_record(project_id: str, record_id: str, payload: ConsensusInput, x_evaluator_token: str | None = Header(default=None)):
        principal = principal_for(project_id, x_evaluator_token)
        # Bind record to the authenticated project before owner action.
        try:
            store.read(record_id, project_id, principal.evaluator_id)
            store.share_for_consensus(record_id, principal.evaluator_id, payload.recipients, project_id=project_id)
        except AccessDenied:
            raise HTTPException(status_code=403, detail="record access denied") from None
        return {"shared": True}

    @app.post("/evaluation/projects/{project_id}/records/{record_id}/revoke")
    def revoke_record(project_id: str, record_id: str, x_evaluator_token: str | None = Header(default=None)):
        principal = principal_for(project_id, x_evaluator_token)
        try:
            store.read(record_id, project_id, principal.evaluator_id)
            store.revoke_consensus(record_id, principal.evaluator_id, project_id=project_id)
        except AccessDenied:
            raise HTTPException(status_code=403, detail="record access denied") from None
        return {"revoked": True}

    return app
