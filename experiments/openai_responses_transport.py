"""Optional OpenAI Responses transport for real-model observation.

Experiment-only provider transport. Runtime remains provider-neutral.
Credentials are read from OPENAI_API_KEY and are never stored in the repository.
"""

from __future__ import annotations

import json
import os
from urllib.request import Request, urlopen

from runtime.real_model_adapter import ModelRequest, RealModelAdapter


DEFAULT_ENDPOINT = "https://api.openai.com/v1/responses"


def openai_responses_transport(request: ModelRequest):
    api_key = os.environ["OPENAI_API_KEY"]
    model = os.environ["OPENAI_MODEL"]
    endpoint = os.environ.get("OPENAI_RESPONSES_URL", DEFAULT_ENDPOINT)

    payload = {
        "model": model,
        "input": request.canonical_prompt,
    }

    http_request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urlopen(http_request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def build_adapter() -> RealModelAdapter:
    return RealModelAdapter(openai_responses_transport)


def main() -> int:
    adapter = build_adapter()
    result = adapter(
        "Observe this input without adding semantic interpretation.",
        "real-model-observation",
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
