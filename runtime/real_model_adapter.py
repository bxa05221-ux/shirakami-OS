"""Provider-neutral boundary for observing a downstream real model.

The adapter owns transport details. Shirakami Runtime does not know the
provider, authentication mechanism, or response schema.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping


@dataclass(frozen=True)
class ModelRequest:
    canonical_prompt: str
    context: Mapping[str, Any] | None = None


class RealModelAdapter:
    """Thin adapter around an externally supplied model transport."""

    def __init__(self, transport: Callable[[ModelRequest], Any]):
        self._transport = transport

    def __call__(self, prompt: str, protocol_id: str) -> Any:
        request = ModelRequest(
            canonical_prompt=prompt,
            context={"protocol_id": protocol_id},
        )
        return self._transport(request)
