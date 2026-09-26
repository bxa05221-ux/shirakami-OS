"""GitHub Copilot SDK provider transport.

The SDK is optional and imported lazily. Authentication remains in the
provider/deployment environment; credentials never enter ProviderRequest,
Evidence, Trace, or AIwitness state.
"""
from __future__ import annotations

from typing import Any

from .provider_transport import ProviderRequest


class CopilotSDKProviderTransport:
    """Async provider transport backed by the GitHub Copilot SDK."""

    def __init__(self, model: str = "gpt-5.4") -> None:
        self.model = model

    async def __call__(self, request: ProviderRequest) -> Any:
        try:
            from copilot import CopilotClient
        except ImportError as exc:
            raise RuntimeError(
                "GitHub Copilot SDK is not installed; install github-copilot-sdk "
                "in the provider runtime before enabling this transport"
            ) from exc

        # Authentication is intentionally delegated to the SDK. In CI it can
        # consume COPILOT_GITHUB_TOKEN / GH_TOKEN / GITHUB_TOKEN; locally it can
        # use the signed-in Copilot CLI credentials.
        client = CopilotClient()
        await client.start()
        try:
            session = await client.create_session(model=self.model)
            try:
                response = await session.send_and_wait(request.canonical_prompt)
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
