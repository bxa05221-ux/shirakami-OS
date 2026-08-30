"""Optional stdlib HTTP wrapper for the OPPAI-Shirakami minimal runtime.

Run: python examples/oppai_api_http.py
Then POST JSON to /v1/chat.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from oppai_shirakami_api_minimal import ShirakamiRuntime, echo_adapter


runtime = ShirakamiRuntime(echo_adapter)


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/v1/chat":
            self._send(404, {"status": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            self._send(400, {"status": "invalid_request"})
            return

        result = runtime.chat(
            payload.get("input"),
            payload.get("context"),
            payload.get("session_id"),
        )
        self._send(200 if result["status"] == "ok" else 400, result)


if __name__ == "__main__":
    print("OPPAI-Shirakami minimal API: http://127.0.0.1:8787/v1/chat")
    HTTPServer(("127.0.0.1", 8787), Handler).serve_forever()
