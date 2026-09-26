"""Provider-neutral real-model adapter boundary.

The Runtime owns context and evidence semantics. A real model is an opaque
downstream backend reached through the ProviderTransport contract.
"""

from __future__ import annotations

from typing import Any

from .provider_transport import (
    ProviderRequest,
    ProviderTransport,
    fixture_provider_transport,
)

# Backward-compatible name for callers/tests that use the model-level request.
ModelRequest = ProviderRequest


class RealModelAdapter:
    """Replaceable model boundary.

    The adapter receives canonical input and returns opaque model output.
    It does not rewrite observations, Evidence, or authority state.
    """

    def __init__(self, transport: ProviderTransport) -> None:
        if not callable(transport):
            raise TypeError("transport must be callable")
        self._transport = transport

    def __call__(self, prompt: str, protocol_id: str) -> Any:
        request = ProviderRequest(
            canonical_prompt=prompt,
            context={"protocol_id": protocol_id},
        )
        return self._transport(request)


def fixture_transport(request: ProviderRequest):
    """Backward-compatible fixture transport alias."""

    return fixture_provider_transport(request)
