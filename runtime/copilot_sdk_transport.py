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
    def __init__(self, model: str = "auto") -> None:
        self.model = model

    async def __call__(self, request: ProviderRequest) -> Any:
        try:
            from copilot import CopilotClient
        except ImportError as exc:
            raise RuntimeError(
                "GitHub Copilot SDK is not installed; install github-copilot-sdk "
                "in the provider runtime before enabling this transport"
            ) from exc
        async with CopilotClient() as client:
            async with await client.create_session(model=self.model) as session:
                response = await session.send_and_wait(request.canonical_prompt)
        if response is None:
            raise RuntimeError("Copilot SDK returned no assistant response")
        content = getattr(getattr(response, "data", None), "content", None)
        if content is None:
            raise RuntimeError("Copilot SDK response did not contain assistant content")
        return {"output": content, "provider": "github-copilot-sdk", "model": self.model}
