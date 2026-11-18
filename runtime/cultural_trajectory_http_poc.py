"""Local-only, candidate-only HTTP projection for synthetic ThreadRPG observations.

No deployment, authentication, Evidence resolution, or remote transport is supplied.
Bind is hard-coded to loopback; do not expose this prototype on a public network.
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from runtime.cultural_trajectory_review import cultural_trajectory_review
from runtime.threadrpg_cultural_trajectory import observe_threadrpg_turn

MAX_BODY_BYTES = 65536


def project_payload(payload: object) -> dict:
    """Project caller-supplied synthetic messages without mutating a thread."""
    if not isinstance(payload, dict) or set(payload) != {"messages"}:
        raise ValueError("expected only 'messages'")
    messages = payload["messages"]
    if not isinstance(messages, list) or not 2 <= len(messages) <= 1000:
        raise ValueError("messages must be a list of 2..1000 posts")
    for item in messages:
        if not isinstance(item, dict) or set(item) != {"id", "text"}:
            raise ValueError("each post needs only id and text")
        if not isinstance(item["id"], str) or not item["id"] or not isinstance(item["text"], str):
            raise ValueError("invalid post")
    return cultural_trajectory_review(observe_threadrpg_turn(messages))


class ObservationHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        if self.path != "/v0/observe":
            self._reply(404, {"error": "not_found"})
            return
        try:
            size = int(self.headers.get("Content-Length", "-1"))
            if not 0 <= size <= MAX_BODY_BYTES:
                self._reply(413, {"error": "invalid_size"})
                return
            raw = self.rfile.read(size)
            payload = json.loads(raw)
            result = project_payload(payload)
        except (ValueError, TypeError, UnicodeDecodeError, json.JSONDecodeError):
            self._reply(400, {"error": "invalid_request"})
            return
        self._reply(200, result)

    def _reply(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        # Never log caller-provided post bodies.
        pass


def serve_local(port: int = 8765) -> None:
    with ThreadingHTTPServer(("127.0.0.1", port), ObservationHandler) as server:
        server.serve_forever()


if __name__ == "__main__":
    serve_local()
