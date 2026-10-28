"""HTTP backend adapter for Universal Model Runtime."""

from __future__ import annotations

import json
from typing import Any, Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .backend import BackendResponse


class UMRBackendError(RuntimeError):
    """Raised when UMR cannot provide a valid execution result."""


class UMRBackend:
    """Execute a Shirakami handoff through the UMR HTTP API."""

    backend_id = "universal-model-runtime:v0.1"

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8766",
        engine: str = "mock",
        timeout: float = 30.0,
        transport: Callable[[Request, float], bytes] | None = None,
    ) -> None:
        if not isinstance(base_url, str) or not base_url.strip():
            raise ValueError("base_url is required")
        if not isinstance(engine, str) or not engine.strip():
            raise ValueError("engine is required")
        if timeout <= 0:
            raise ValueError("timeout must be positive")

        self._base_url = base_url.rstrip("/")
        self._engine = engine
        self._timeout = timeout
        self._transport = transport or self._request

    def execute(self, handoff: Mapping[str, Any]) -> BackendResponse:
        if not isinstance(handoff, Mapping):
            raise TypeError("handoff must be a mapping")

        model_input = self._model_input(handoff)
        request_body = {
            "engine": self._engine,
            "input": {"text": model_input},
        }

        request = Request(
            f"{self._base_url}/v1/execute",
            data=json.dumps(
                request_body,
                ensure_ascii=False,
                sort_keys=True,
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            raw = self._transport(request, self._timeout)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise UMRBackendError("UMR request failed") from exc

        try:
            result = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise UMRBackendError("UMR returned invalid JSON") from exc

        if not isinstance(result, dict):
            raise UMRBackendError("UMR response must be a JSON object")
        if result.get("status") != "success":
            raise UMRBackendError("UMR execution was not successful")
        if result.get("engine") != self._engine:
            raise UMRBackendError("UMR response engine did not match request")

        output = result.get("output")
        if not isinstance(output, dict):
            raise UMRBackendError("UMR response output must be an object")

        payload: dict[str, Any] = {
            "engine": self._engine,
            "output": output,
        }
        request_id = handoff.get("request_id")
        if request_id is not None:
            payload["request_id"] = request_id

        return BackendResponse(
            backend_id=self.backend_id,
            status="completed",
            payload=payload,
        )

    @staticmethod
    def _model_input(handoff: Mapping[str, Any]) -> str:
        """Serialize only task input and explicitly admitted context."""
        if "input" in handoff:
            task_input = handoff["input"]
        elif "payload" in handoff:
            task_input = handoff["payload"]
        else:
            raise ValueError("handoff must contain input or payload")

        document: dict[str, Any] = {"task_input": task_input}
        if "context_bundle" in handoff:
            document["context_bundle"] = handoff["context_bundle"]
        if "previous_outputs" in handoff:
            document["previous_outputs"] = handoff["previous_outputs"]

        try:
            return json.dumps(
                document,
                ensure_ascii=False,
                sort_keys=True,
            )
        except (TypeError, ValueError) as exc:
            raise ValueError("handoff model input must be JSON-serializable") from exc

    @staticmethod
    def _request(request: Request, timeout: float) -> bytes:
        with urlopen(request, timeout=timeout) as response:
            return response.read()
