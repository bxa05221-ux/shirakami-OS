"""Minimal OpenAI Responses API backend adapter for Shirakami Runtime.

Provider-specific HTTP details live here; Runtime Core consumes only BackendResponse.
"""

import json
from typing import Any, Callable, Mapping
from urllib.request import Request, urlopen

from aiwitness.policy_gate import AIwitnessPolicyGate, AuthorizedHandoff, PolicyDenied
from .backend import BackendResponse


class OpenAIBackend:
    """External OpenAI backend implementing the provider-neutral backend shape."""

    backend_id = "openai-responses:v0.1"

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-5.6-luna",
        endpoint: str = "https://api.openai.com/v1/responses",
        transport: Callable[[Request], bytes] | None = None,
        policy_gate: AIwitnessPolicyGate | None = None,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")
        self._api_key = api_key
        self._model = model
        self._endpoint = endpoint
        self._transport = transport or self._request
        self._policy_gate = policy_gate

    def execute(self, handoff: Mapping[str, Any]) -> BackendResponse:
        if self._policy_gate is None:
            raise PolicyDenied("AIwitness policy gate is required for external provider use")
        authorized: AuthorizedHandoff = self._policy_gate.authorize(handoff, provider="openai", model=self._model)
        self._policy_gate.verify(authorized, provider="openai", model=self._model)
        request_id = handoff.get("request_id")
        payload = {
            "model": self._model,
            "input": authorized.payload,
        }
        request = Request(
            self._endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        raw = self._transport(request)
        response_payload = json.loads(raw.decode("utf-8"))
        observed = dict(response_payload)
        if request_id is not None:
            observed["request_id"] = request_id
        return BackendResponse(
            backend_id=self.backend_id,
            status="completed",
            payload=observed,
        )

    @staticmethod
    def _request(request: Request) -> bytes:
        with urlopen(request, timeout=60) as response:
            return response.read()
