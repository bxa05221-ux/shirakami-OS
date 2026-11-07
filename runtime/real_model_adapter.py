"""Provider-neutral real-model adapter boundary.

The Runtime owns context and evidence semantics. A real model is an opaque
downstream backend reached through the ProviderTransport contract.
"""

from __future__ import annotations

from typing import Any, Mapping

from .adapter import PipelineAdapterRequest
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

    def __call__(
        self,
        prompt: str,
        protocol_id: str,
        *,
        generation_control: Mapping[str, Any] | None = None,
    ) -> Any:
        """Send canonical input without interpreting protocol control.

        ``generation_control`` is optional so existing two-argument callers
        retain their original ProviderRequest shape.  When supplied, it is
        copied verbatim as request-scoped model context; this adapter neither
        evaluates it nor turns it into Evidence, Reality mutation, or
        authority.
        """
        context: dict[str, Any] = {"protocol_id": protocol_id}
        if generation_control is not None:
            if not isinstance(generation_control, Mapping):
                raise TypeError("generation_control must be a mapping")
            context["generation_control"] = dict(generation_control)
        request = ProviderRequest(
            canonical_prompt=prompt,
            context=context,
        )
        return self._transport(request)

    def execute_pipeline(self, request: PipelineAdapterRequest) -> Any:
        """Adapt one explicit Pipeline step to the provider boundary.

        This is intentionally a data-only handoff.  The Pipeline remains the
        source of phase/action/context; the provider only receives a copied,
        request-scoped generation-control envelope.
        """
        prompt = request.input.get("canonical_prompt")
        if not isinstance(prompt, str):
            raise ValueError("pipeline request requires input.canonical_prompt")

        inherited = request.context.get("generation_control", {})
        if not isinstance(inherited, Mapping):
            raise TypeError("context.generation_control must be a mapping")
        generation_control = dict(inherited)
        generation_control.update(
            {
                "protocol_id": request.protocol_id,
                "protocol_version": request.version,
                "phase": request.phase,
                "action": request.action,
            }
        )
        return self(
            prompt,
            request.protocol_id,
            generation_control=generation_control,
        )


def fixture_transport(request: ProviderRequest):
    """Backward-compatible fixture transport alias."""

    return fixture_provider_transport(request)
