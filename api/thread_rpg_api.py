"""HTTP boundary for the Thread RPG 3.2 runtime slice."""

from typing import Any

from runtime.thread_rpg import ThreadRenderer, ThreadRuntime


def create_app(runtime: ThreadRuntime | None = None):
    """Create a small FastAPI application for Thread RPG sessions."""
    from fastapi import FastAPI, HTTPException

    thread_runtime = runtime or ThreadRuntime()
    app = FastAPI(title="Shirakami Thread RPG", version="3.2.0")

    @app.post("/sessions")
    def create_session(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            state = thread_runtime.create_session(payload.get("landscape_ref", ""))
            return {"session_id": state.session_id, "status": state.status}
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/sessions/{session_id}/turns")
    def submit_turn(session_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            turn, state, evidence = thread_runtime.submit_turn(
                session_id,
                payload.get("participant_input", ""),
                payload.get("participant", "human"),
            )
            return {
                "turn": turn.__dict__,
                "state": state.snapshot(),
                "evidence": {
                    "protocol_id": evidence.protocol_id,
                    "transition_kind": evidence.transition_kind,
                    "transition_data": dict(evidence.transition_data),
                    "signals": list(evidence.signals),
                },
            }
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="session not found") from exc
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/sessions/{session_id}/state")
    def get_state(session_id: str) -> dict[str, Any]:
        try:
            return dict(ThreadRenderer.render(thread_runtime.get_state(session_id)))
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="session not found") from exc

    @app.get("/sessions/{session_id}/evidence")
    def get_evidence(session_id: str) -> list[dict[str, Any]]:
        try:
            return [
                {
                    "protocol_id": item.protocol_id,
                    "status": item.status,
                    "transition_kind": item.transition_kind,
                    "transition_data": dict(item.transition_data),
                    "signals": list(item.signals),
                    "confidence": item.confidence,
                }
                for item in thread_runtime.evidence(session_id)
            ]
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="session not found") from exc

    return app
