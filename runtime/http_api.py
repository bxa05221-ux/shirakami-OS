"""Dependency-free HTTP API boundary for the Shirakami Landscape pipeline."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

from .context_boundary import create_context_snapshot
from .landscape import LandscapeState
from .project_landscape_assembly import assemble_landscape
from .project_landscape_loader import load_landscape
from .protocol_applicability import evaluate_applicability
from .protocol_input import create_protocol_input
from .protocol_ir import build_protocol_ir
from .protocol_runtime import execute_protocol_ir
from .prototype import Transition
from .source_registry import build_registry


class ShirakamiSessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, dict[str, Any]] = {}

    def create(
        self,
        session_id: str,
        landscape_ref: str,
        landscape: dict[str, Any] | None = None,
        *,
        sources: list[dict[str, object]] | None = None,
        source_contents: dict[str, object] | None = None,
        applicability_conditions: dict[str, object] | None = None,
        applicability_available: dict[str, object] | None = None,
    ) -> dict[str, Any]:
        if session_id in self._sessions:
            raise ValueError("session already exists")

        raw_sources = sources or []
        contents = source_contents or {}
        registry = build_registry(raw_sources)
        loaded = load_landscape(registry, contents)
        project_landscape = assemble_landscape(loaded.sources, loaded.unresolved_questions)
        context = create_context_snapshot(
            project_landscape,
            context_id=session_id,
            parent_landscape_ref=landscape_ref,
            requested_context="http-api",
        )
        self._sessions[session_id] = {
            "session_id": session_id,
            "landscape_ref": landscape_ref,
            "landscape": LandscapeState.from_snapshot(landscape or {}),
            "project_landscape": project_landscape,
            "context": context,
            "applicability_conditions": applicability_conditions or {},
            "applicability_available": applicability_available or {},
            "evidence": [],
            "turns": [],
        }
        return self.state(session_id)

    def state(self, session_id: str) -> dict[str, Any]:
        session = self._sessions[session_id]
        context = session["context"]
        return {
            "session_id": session["session_id"],
            "landscape_ref": session["landscape_ref"],
            "landscape": dict(session["landscape"].snapshot()),
            "turn_count": len(session["turns"]),
            "context": {
                "context_id": context.context_id,
                "parent_landscape_ref": context.parent_landscape_ref,
                "source_ids": [item.source.ref.id for item in context.source_refs],
                "unresolved_questions": list(context.unresolved_questions),
            },
        }

    def evidence(self, session_id: str) -> list[dict[str, Any]]:
        return [
            {
                "protocol_id": item.protocol_id,
                "status": item.status,
                "transition_kind": item.transition_kind,
                "transition_data": dict(item.transition_data),
                "signals": list(item.signals),
                "confidence": item.confidence,
            }
            for item in self._sessions[session_id]["evidence"]
        ]

    def turn(self, session_id: str, text: str) -> dict[str, Any]:
        session = self._sessions[session_id]
        context = create_protocol_input(session["context"])
        applicability = evaluate_applicability(
            context,
            "thread.http.turn",
            session["applicability_conditions"],
            available=session["applicability_available"],
        )
        if not applicability.applicable:
            return {
                "status": "not_applicable",
                "protocol_id": "thread.http.turn",
                "unresolved_questions": list(applicability.unresolved_questions),
                "failed_conditions": list(applicability.failed_conditions),
                "state": self.state(session_id),
            }

        ir = build_protocol_ir(
            context,
            protocol_id="thread.http.turn",
            transition_kind="thread.turn_added",
            transition_data={"changed": True, "text": text},
        )

        def declared_transition(_context) -> Transition:
            return Transition(kind=ir.transition_kind, data=ir.transition_data)

        execution = execute_protocol_ir(ir, declared_transition)
        evidence = execution.evidence
        if execution.result.status == "completed":
            session["landscape"].apply_evidence(evidence)
            session["evidence"].append(evidence)
            session["turns"].append(text)

        return {
            "status": execution.result.status,
            "protocol_id": execution.result.protocol_id,
            "transition_kind": evidence.transition_kind,
            "transition_data": dict(evidence.transition_data),
            "state": self.state(session_id),
        }


class ShirakamiRequestHandler(BaseHTTPRequestHandler):
    store = ShirakamiSessionStore()

    def _write_json(self, status: int, payload: Any) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        path = urlparse(self.path).path.rstrip("/")
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            if path == "/sessions":
                result = self.store.create(
                    payload["session_id"],
                    payload["landscape_ref"],
                    payload.get("landscape"),
                    sources=payload.get("sources"),
                    source_contents=payload.get("source_contents"),
                    applicability_conditions=payload.get("applicability_conditions"),
                    applicability_available=payload.get("applicability_available"),
                )
                self._write_json(201, result)
                return
            parts = path.split("/")
            if len(parts) == 4 and parts[1] == "sessions" and parts[3] == "turns":
                result = self.store.turn(parts[2], payload["text"])
                self._write_json(200, result)
                return
            self._write_json(404, {"error": "not found"})
        except KeyError as exc:
            self._write_json(400, {"error": f"missing field: {exc.args[0]}"})
        except Exception as exc:
            self._write_json(400, {"error": str(exc)})

    def do_GET(self) -> None:
        path = urlparse(self.path).path.rstrip("/")
        parts = path.split("/")
        try:
            if len(parts) == 4 and parts[1] == "sessions" and parts[3] == "state":
                self._write_json(200, self.store.state(parts[2]))
                return
            if len(parts) == 4 and parts[1] == "sessions" and parts[3] == "evidence":
                self._write_json(200, self.store.evidence(parts[2]))
                return
            self._write_json(404, {"error": "not found"})
        except KeyError:
            self._write_json(404, {"error": "session not found"})


def serve(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), ShirakamiRequestHandler)
    print(f"Shirakami HTTP API listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    serve()
