"""Provider-neutral real-model adapter boundary.

The Runtime owns context and evidence semantics. A real model is an opaque
downstream backend reached through this adapter contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping


@dataclass(frozen=True)
class ModelRequest:
    """Canonical request crossing from Shirakami Runtime to a model."""

    canonical_prompt: str
    context: Mapping[str, Any]


class RealModelAdapter:
    """Replaceable model boundary.

    The adapter receives canonical input and returns opaque model output.
    It does not rewrite observations, Evidence, or authority state.
    """

    def __init__(self, transport: Callable[[ModelRequest], Any]) -> None:
        if not callable(transport):
            raise TypeError("transport must be callable")
        self._transport = transport

    def __call__(self, prompt: str, protocol_id: str) -> Any:
        request = ModelRequest(
            canonical_prompt=prompt,
            context={"protocol_id": protocol_id},
        )
        return self._transport(request)


def fixture_transport(request: ModelRequest) -> Mapping[str, Any]:
    """Deterministic provider-neutral transport for boundary verification."""
    return {
        "output": request.canonical_prompt,
        "provider": "fixture",
        "protocol_id": request.context["protocol_id"],
    }
