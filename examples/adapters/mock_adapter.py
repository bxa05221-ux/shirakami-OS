"""Deterministic adapter for local smoke tests."""


def mock_adapter(input_text: str, context: dict) -> str:
    return f"[mock] {input_text}"
