"""HTTP-facing API boundary for the completed AATS Wayfinding cycle."""

from __future__ import annotations

import json
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Mapping

from .aats import Participant, Post, Thread
from .aat_thread_wayfinding import run_aats_wayfinding
from .landscape import LandscapeState
from .prototype import Transition
from .way import SmallStep


class _RequestSelector:
    def __init__(self, step: SmallStep) -> None:
        self.step = step

    def select(self, landscape: Mapping[str, object]) -> SmallStep:
        return self.step


class _RequestApplier:
    def __init__(self, transition: Transition) -> None:
        self.transition = transition

    def apply(self, step: SmallStep) -> Transition:
        return self.transition


class _StateObserver:
    def observe(self, state: LandscapeState) -> Mapping[str, object]:
        return state.snapshot()


def _thread_from_payload(payload: Mapping[str, Any]) -> Thread:
    participants = tuple(
        Participant(str(item["participant_id"]), item.get("persona"))
        for item in payload.get("participants", [])
    )
    posts = tuple(
        Post(str(item["participant_id"]), str(item["text"]), item.get("aa"))
        for item in payload.get("posts", [])
    )
    return Thread(str(payload["thread_id"]), participants, posts)


def execute_wayfinding_request(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Execute one transport-level Wayfinding request."""
    thread = _thread_from_payload(payload["thread"])
    state = LandscapeState.from_snapshot(payload.get("landscape", {}))
    step_data = payload["small_step"]
    step = SmallStep(str(step_data["action"]), step_data.get("reason"))
    transition_data = dict(payload.get("transition", {}).get("data", {}))
    transition_data.setdefault("changed", True)
    transition = Transition(
        kind=str(payload.get("transition", {}).get("kind", "wayfinding.small_step")),
        data=transition_data,
    )
    result = run_aats_wayfinding(
        thread, state, _RequestSelector(step), _RequestApplier(transition), _StateObserver()
    )
    return {
        "viewpoints": [asdict(viewpoint) for viewpoint in result.viewpoints],
        "narrative": result.narrative,
        "before": dict(result.before),
        "small_step": asdict(result.small_step),
        "evidence": asdict(result.evidence),
        "after": dict(result.after),
    }


class WayfindingAPIHandler(BaseHTTPRequestHandler):
    """Minimal stdlib HTTP adapter; framework-independent by design."""

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/wayfinding":
            self.send_error(404, "unknown endpoint")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            body = json.dumps(execute_wayfinding_request(payload), ensure_ascii=False).encode("utf-8")
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            self.send_error(400, str(exc))
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8080) -> None:
    server = ThreadingHTTPServer((host, port), WayfindingAPIHandler)
    server.serve_forever()


if __name__ == "__main__":
    serve()
