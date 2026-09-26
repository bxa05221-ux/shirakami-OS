"""Provider-neutral transport contract for real-model adapters.

The provider transport is an opaque downstream boundary. Shirakami owns
context, Evidence, traceability, and authority semantics; the transport
only carries a canonical model request to a replaceable provider backend.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol


@dataclass(frozen=True)
class ProviderRequest:
    """Canonical request crossing the provider boundary."""

    canonical_prompt: str
    context: Mapping[str, Any]


class ProviderTransport(Protocol):
    """Replaceable provider transport contract.

    Implementations MUST return opaque provider output and MUST NOT mutate
    Shirakami Evidence, trace, observation, or authority state.
    """

    def __call__(self, request: ProviderRequest) -> Any:
        """Send a canonical request and return opaque provider output."""
        ...


def fixture_provider_transport(request: ProviderRequest) -> Mapping[str, Any]:
    """Deterministic transport used for boundary verification."""

    return {
        "output": request.canonical_prompt,
        "provider": "fixture",
        "protocol_id": request.context["protocol_id"],
    }
