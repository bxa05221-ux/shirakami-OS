"""Minimal OPPAI-Shirakami runtime reference."""

from typing import Any, Callable

from src.shirakami.oppai import listen
from src.shirakami.session import SessionStore


class ShirakamiRuntime:
    def __init__(self, model_adapter: Callable[[str, dict[str, Any]], str], session_store: SessionStore | None = None):
        self.model_adapter = model_adapter
        self.session_store = session_store or SessionStore()

    def chat(self, input_text: str, context: dict[str, Any] | None = None, session_id: str | None = None) -> dict[str, Any]:
        if not isinstance(input_text, str) or not input_text.strip():
            return {"response": None, "session_id": session_id, "context_delta": {}, "status": "invalid_request"}

        session_context = self.session_store.get(session_id) if session_id else {}
        merged_context = {**session_context, **(context or {})}
        envelope = listen(input_text, merged_context)
        response = self.model_adapter(envelope.raw_input, envelope.context)

        context_delta = {"last_input": envelope.raw_input}
        if session_id:
            self.session_store.update(session_id, context_delta)

        return {"response": response, "session_id": session_id, "context_delta": context_delta, "status": "ok"}


def echo_adapter(input_text: str, context: dict[str, Any]) -> str:
    return input_text


if __name__ == "__main__":
    runtime = ShirakamiRuntime(echo_adapter)
    print(runtime.chat("こんにちは。普通に話してみる。", {"demo": True}, "demo-001"))
