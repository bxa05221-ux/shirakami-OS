"""Minimal OPPAI-Shirakami runtime reference.

The public boundary accepts natural language. OPPAI captures the raw input
and context before the provider-specific model adapter is invoked.
"""

from typing import Any, Callable

from src.shirakami.oppai import listen


class ShirakamiRuntime:
    def __init__(self, model_adapter: Callable[[str, dict[str, Any]], str]):
        self.model_adapter = model_adapter

    def chat(
        self,
        input_text: str,
        context: dict[str, Any] | None = None,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        if not isinstance(input_text, str) or not input_text.strip():
            return {
                "response": None,
                "session_id": session_id,
                "context_delta": {},
                "status": "invalid_request",
            }

        envelope = listen(input_text, context)
        response = self.model_adapter(envelope.raw_input, envelope.context)

        return {
            "response": response,
            "session_id": session_id,
            "context_delta": {},
            "status": "ok",
        }


def echo_adapter(input_text: str, context: dict[str, Any]) -> str:
    """Deterministic adapter used only to verify the boundary locally."""
    return input_text


if __name__ == "__main__":
    runtime = ShirakamiRuntime(echo_adapter)
    print(runtime.chat("こんにちは。普通に話してみる。", {"demo": True}, "demo-001"))
