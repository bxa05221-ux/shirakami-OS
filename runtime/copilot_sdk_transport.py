"""GitHub Copilot SDK provider transport.

The SDK is optional and imported lazily. Authentication remains in the
provider/deployment environment; credentials never enter ProviderRequest,
Evidence, Trace, or AIwitness state.
"""
from __future__ import annotations

import os
from typing import Any

from aiwitness.policy_gate import AIwitnessPolicyGate, PolicyDenied
from .provider_transport import ProviderRequest


class CopilotSDKProviderTransport:
    """Async provider transport backed by the GitHub Copilot SDK."""

    def __init__(self, model: str = "gpt-5.4", policy_gate: AIwitnessPolicyGate | None = None) -> None:
        self.model = model
        self._policy_gate = policy_gate

    async def __call__(self, request: ProviderRequest) -> Any:
        if self._policy_gate is None:
            raise PolicyDenied("AIwitness policy gate is required for external provider use")
        classification = request.context.get("data_classification", "unknown")
        authorized = self._policy_gate.authorize(
            {"input": request.canonical_prompt, "data_classification": classification},
            provider="github-copilot-sdk", model=self.model,
        )
        self._policy_gate.verify(authorized, provider="github-copilot-sdk", model=self.model)
        try:
            from copilot import CopilotClient
        except ImportError as exc:
            raise RuntimeError(
                "GitHub Copilot SDK is not installed; install github-copilot-sdk "
                "in the provider runtime before enabling this transport"
            ) from exc

        # Explicit token auth for CI; otherwise allow the SDK's local signed-in
        # CLI flow. The token is never copied into ProviderRequest or evidence.
        token = (
            os.getenv("COPILOT_GITHUB_TOKEN")
            or os.getenv("GH_TOKEN")
            or os.getenv("GITHUB_TOKEN")
        )
        client = (
            CopilotClient({
                "github_token": token,
                "use_logged_in_user": False,
            })
            if token
            else CopilotClient()
        )
        await client.start()
        try:
            session = await client.create_session(model=self.model)
            try:
                response = await session.send_and_wait(authorized.payload)
            finally:
                await session.disconnect()
        finally:
            await client.stop()

        if response is None:
            raise RuntimeError("Copilot SDK returned no assistant response")
        content = getattr(getattr(response, "data", None), "content", None)
        if content is None:
            raise RuntimeError("Copilot SDK response did not contain assistant content")
        return {
            "output": content,
            "provider": "github-copilot-sdk",
            "model": self.model,
        }
