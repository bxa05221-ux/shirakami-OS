"""Minimal external-AI adapter round-trip control.

This experiment does not add production semantics. It verifies that the
existing Runtime output can cross an Adapter-shaped boundary to an external
AI stand-in and that the external response can cross back as an observable
result.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.prototype import Runtime, Transition


@dataclass(frozen=True)
class AIRequest:
    protocol_id: str
    input: Mapping[str, Any]
    transition_kind: str


@dataclass(frozen=True)
class AIResponse:
    protocol_id: str
    output: Mapping[str, Any]


class ExternalAIAdapter:
    """Test-only connection point between Runtime and an external AI."""

    def send(self, request: AIRequest) -> AIResponse:
        # External-AI stand-in: it returns the received request without
        # inventing Shirakami semantics.
        return AIResponse(
            protocol_id=request.protocol_id,
            output={"received": True, "transition_kind": request.transition_kind},
        )


def protocol(_context) -> Transition:
    return Transition(
        kind="adapter.roundtrip",
        data={"message": "hello external ai"},
    )


def main() -> int:
    runtime = Runtime()
    result = runtime.execute("adapter.roundtrip", protocol, {"message": "hello"})
    assert result.status == "completed"

    adapter = ExternalAIAdapter()
    request = AIRequest(
        protocol_id=result.protocol_id,
        input={"message": "hello"},
        transition_kind=result.transition.kind,
    )
    response = adapter.send(request)

    assert response.protocol_id == result.protocol_id
    assert response.output["received"] is True
    assert response.output["transition_kind"] == result.transition.kind

    print("RUNTIME", result.status, result.protocol_id)
    print("ADAPTER_OUT", dict(response.output))
    print("AI_ROUNDTRIP", "VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
