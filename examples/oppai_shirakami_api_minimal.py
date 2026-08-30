"""Minimal reference server for the OPPAI-Shirakami API contract.

No vendor SDK is required. The model adapter is intentionally a callable so
that any LLM/provider can be connected without changing the public boundary.
"""

from typing import Any, Callable


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
            return {"response": None, "session_id": session_id, "context_delta": {}, "status": "invalid_request"}

        ctx = context or {}
        # Minimal OPPAI boundary: preserve the user's natural input and context
        # rather than requiring provider-specific prompt syntax.
        response = self.model_adapter(input_text, ctx)
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
