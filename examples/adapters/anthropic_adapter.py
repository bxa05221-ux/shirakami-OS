"""Minimal Anthropic Messages API adapter for Shirakami Runtime.

Requires: ANTHROPIC_API_KEY environment variable.
The Runtime-facing contract stays model/provider agnostic.
"""

import json
import os
from urllib.request import Request, urlopen


class AnthropicAdapter:
    def __init__(self, model: str = "claude-3-5-haiku-latest"):
        self.model = model
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is required")

    def __call__(self, input_text: str, context: dict) -> str:
        request = Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps({
                "model": self.model,
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": input_text}],
            }).encode("utf-8"),
            headers={
                "content-type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )
        with urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return "".join(
            block.get("text", "")
            for block in payload.get("content", [])
            if block.get("type") == "text"
        )
