"""Exercise a real Copilot response through the Shirakami HTTP boundary.

Without a provider credential, the script runs a deterministic fixture check.
With COPILOT_GITHUB_TOKEN, it invokes the GitHub Copilot SDK from inside the
HTTP request's async provider adapter; the model output is not pre-injected.
"""
from __future__ import annotations

import asyncio
import os
import uuid
from typing import Any

from fastapi.testclient import TestClient

from api.http import ShirakamiHTTPTransport
from runtime.api import ShirakamiAPI
from runtime.evolution_bridge import ContextSnapshot
from runtime.prototype import Transition
from runtime.provider_transport import ProviderRequest
from runtime.copilot_sdk_transport import CopilotSDKProviderTransport

API_KEY = "local-observation-key"
PROTOCOL_ID = "copilot.http.observation"
HANDOFF_ID = "SH-HO-COPILOT-HTTP-001"


def observation_protocol(context: Any) -> Transition:
    return Transition(
        kind=PROTOCOL_ID,
        data={
            "provider_output_received": context.input.get("provider_output") is not None,
        },
    )


def assert_boundary(client: TestClient, body: dict[str, Any], trace_id: str) -> None:
    evidence_ids = body.get("evidence_ids") or []
    if len(evidence_ids) != 1:
        raise AssertionError(f"expected exactly one linked Evidence ID; got {evidence_ids!r}")
    evidence_id = evidence_ids[0]

    headers = {"X-API-Key": API_KEY}
    evidence_response = client.get(f"/v1/evidence/{evidence_id}", headers=headers)
    trace_response = client.get(f"/v1/traces/{trace_id}", headers=headers)
    witness_response = client.get(f"/v1/witnesses/{trace_id}", headers=headers)
    traceability_response = client.get(f"/v1/traceability/{trace_id}", headers=headers)
    for response in (evidence_response, trace_response, witness_response, traceability_response):
        response.raise_for_status()

    evidence = evidence_response.json()
    trace = trace_response.json()
    witness = witness_response.json()
    traceability = traceability_response.json()
    if evidence.get("model_output") != body.get("model_output"):
        raise AssertionError("HTTP model output does not match stored Evidence")
    if trace.get("evidence_ids") != [evidence_id]:
        raise AssertionError("Trace does not reference the exact Evidence ID")
    if witness.get("evidence_ids") != [evidence_id]:
        raise AssertionError("AIwitness does not reference the exact Evidence ID")
    if traceability.get("valid") is not True:
        raise AssertionError("traceability verification did not return valid=true")

    if body.get("execution_authorized") is not False:
        raise AssertionError("execution_authorized must remain false")
    if body.get("publish_authorized") is not False:
        raise AssertionError("publish_authorized must remain false")
    if body.get("merge_authorized") is not False:
        raise AssertionError("merge_authorized must remain false")
    if body.get("human_gate_required") is not True:
        raise AssertionError("human_gate_required must remain true")

    print("BOUNDARY_OBSERVED=true")
    print(f"PROVIDER={body['model_output'].get('provider', 'unknown')}")
    print(f"EVIDENCE_ID={evidence_id}")
    print(f"TRACE_ID={trace_id}")
    print("AUTHORITY=human_gate_required")
    print("TRACEABILITY_VALID=true")


async def main() -> None:
    token = os.getenv("COPILOT_GITHUB_TOKEN") or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    live = bool(token)
    require_live = os.getenv("REQUIRE_LIVE_PROVIDER", "").strip().lower() in {"1", "true", "yes"}
    if require_live and not live:
        raise SystemExit(
            "REQUIRE_LIVE_PROVIDER=true but no Copilot credential is configured; "
            "refusing to report fixture mode as a live-provider test"
        )
    trace_id = f"TRACE-COPILOT-HTTP-{uuid.uuid4().hex[:12]}"

    if live:
        provider_transport = CopilotSDKProviderTransport(model="gpt-5.4")

        async def provider_adapter(prompt: str, protocol_id: str) -> dict[str, Any]:
            # The SDK call occurs inside the HTTP request's async adapter.
            # Its response, not a pre-injected fixture value, enters Runtime.
            return await provider_transport(
                ProviderRequest(
                    canonical_prompt=prompt,
                    context={"protocol_id": protocol_id},
                )
            )
    else:
        async def provider_adapter(prompt: str, protocol_id: str) -> dict[str, str]:
            return {
                "output": f"fixture:{prompt}",
                "provider": "fixture-async",
                "protocol_id": protocol_id,
            }

    api = ShirakamiAPI()
    api.observe(
        {"signal": "execute"},
        ContextSnapshot(
            protocol_id=PROTOCOL_ID,
            landscape={},
            metadata={"source": "copilot-http-observation"},
        ),
    )
    api.analyze(PROTOCOL_ID, protocol_exists=True)

    transport = ShirakamiHTTPTransport(
        api=api,
        protocol_registry={PROTOCOL_ID: observation_protocol},
        api_key=API_KEY,
        async_model_adapter=provider_adapter,
    )
    client = TestClient(transport.create_app())
    payload = {
        "protocol_id": PROTOCOL_ID,
        "input_data": {"text": "Observe provider output through Shirakami HTTP"},
        "handoff_id": HANDOFF_ID,
        "trace_id": trace_id,
        "evidence_ids": [],
        "boundary_context": {
            "handoff_id": HANDOFF_ID,
            "project": "Shirakami API MVP",
            "objective": "Verify provider output through HTTP, Evidence, Trace, and AIwitness",
            "protocol_ids": [PROTOCOL_ID],
            "evidence_ids": [],
            "verification_scope": ["HTTP", "Copilot", "Runtime", "Evidence", "Trace", "AIwitness"],
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
            "human_gate_required": True,
        },
    }
    response = client.post(
        "/v1/execute",
        json=payload,
        headers={"X-API-Key": API_KEY},
    )
    response.raise_for_status()
    body = response.json()
    output = body.get("model_output")
    if not isinstance(output, dict) or not isinstance(output.get("output"), str) or not output["output"].strip():
        raise AssertionError("HTTP execution did not return non-empty provider output")

    assert_boundary(client, body, trace_id)
    print(f"LIVE_PROVIDER_OBSERVED={'true' if live else 'false'}")
    if not live:
        print("reason=no provider credential configured; fixture path only")


if __name__ == "__main__":
    asyncio.run(main())
