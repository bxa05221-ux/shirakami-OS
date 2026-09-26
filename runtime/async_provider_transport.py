"""Async provider boundary for SDK-backed model transports.

Some provider SDKs, including the current GitHub Copilot Python SDK, expose
native async APIs. This module keeps that execution model explicit instead of
hiding an event loop inside the synchronous Runtime contract.
"""

from __future__ import annotations

from typing import Any, Awaitable, Protocol

from .provider_transport import ProviderRequest


class AsyncProviderTransport(Protocol):
    """Replaceable async provider transport contract."""

    def __call__(self, request: ProviderRequest) -> Awaitable[Any]:
        """Send a canonical request and return opaque provider output."""
        ...


async def fixture_async_provider_transport(request: ProviderRequest) -> dict[str, Any]:
    """Deterministic async transport used for boundary verification."""

    return {
        "output": request.canonical_prompt,
        "provider": "fixture-async",
        "protocol_id": request.context["protocol_id"],
    }
