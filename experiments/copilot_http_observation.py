"""Copilot provider observation harness.

Fixture mode verifies the Shirakami HTTP -> Runtime -> Evidence -> Trace ->
AIwitness boundary without credentials. Live mode obtains one real Copilot
response and routes that opaque output through the same boundary.
"""
from __future__ import annotations

import argparse
import asyncio
import os

from fastapi.testclient import TestClient

from api.http import ShirakamiHTTPTransport
from runtime.api import ShirakamiAPI
from runtime.evolution_bridge import ContextSnapshot
from runtime.prototype import Transition

API_KEY = "local-observation-key"
PROTOCOL_ID = "copilot.live.observation"
TRACE_ID = "TRACE-COPILOT-LIVE-001"
HANDOFF_ID = "SH-HO-COPILOT-LIVE-001"


def protocol(context):
    return Transition(
        kind=PROTOCOL_ID,
        data={"provider_output_received": context.input.get("provider_output") is not None},
    )


def observe_output(content: str, provider: str) -> None:
    api = ShirakamiAPI()
    api.observe({"signal": "execute"}, ContextSnapshot(protocol_id=PROTOCOL_ID, landscape={}, metadata={"source": "copilot-observation"}))
    api.analyze(PROTOCOL_ID, protocol_exists=True)
    transport = ShirakamiHTTPTransport(api=api,
        protocol_registry={PROTOCOL_ID: protocol},
        api_key=API_KEY,
        model_adapter=lambda _prompt, _protocol_id: {
            "output": content,
            "provider": provider,
        },
    )
    http = TestClient(transport.create_app())
    payload = {
        "protocol_id": PROTOCOL_ID,
        "input_data": {
            "text": "Copilot provider observation",
            "provider_output": content,
        },
        "handoff_id": HANDOFF_ID,
        "trace_id": TRACE_ID,
        "evidence_ids": [],
        "boundary_context": {
            "handoff_id": HANDOFF_ID,
            "project": "Shirakami API MVP",
            "objective": "Observe provider output through the Shirakami evidence boundary",
            "protocol_ids": [PROTOCOL_ID],
            "evidence_ids": [],
            "verification_scope": [
                "Copilot",
                "HTTP",
                "Runtime",
                "Evidence",
                "Trace",
                "AIwitness",
            ],
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
            "human_gate_required": True,
        },
    }
    result = http.post(
        "/v1/execute",
        json=payload,
        headers={"X-API-Key": API_KEY},
    )
    result.raise_for_status()
    body = result.json()

    evidence_id = body["evidence_ids"][0]
    evidence = http.get(
        f"/v1/evidence/{evidence_id}",
        headers={"X-API-Key": API_KEY},
    )
    trace = http.get(
        f"/v1/traces/{TRACE_ID}",
        headers={"X-API-Key": API_KEY},
    )
    witness = http.get(
        f"/v1/witnesses/{TRACE_ID}",
        headers={"X-API-Key": API_KEY},
    )
    traceability = http.get(
        f"/v1/traceability/{TRACE_ID}",
        headers={"X-API-Key": API_KEY},
    )

    evidence.raise_for_status()
    trace.raise_for_status()
    witness.raise_for_status()
    traceability.raise_for_status()

    evidence_body = evidence.json()
    trace_body = trace.json()
    witness_body = witness.json()
    traceability_body = traceability.json()
    stored_output = evidence_body.get("model_output")
    if stored_output != {"output": content, "provider": provider}:
        raise AssertionError("provider output was not preserved exactly in Evidence")
    if trace_body.get("evidence_ids") != [evidence_id]:
        raise AssertionError("Trace does not reference the stored Evidence ID")
    if witness_body.get("evidence_ids") != [evidence_id]:
        raise AssertionError("AIwitness does not reference the stored Evidence ID")
    if traceability_body.get("valid") is not True:
        raise AssertionError("traceability validation did not succeed")

    if body["execution_authorized"] is not False:
        raise AssertionError("execution authority boundary changed")
    if body["human_gate_required"] is not True:
        raise AssertionError("Human Gate boundary changed")

    print("BOUNDARY_OBSERVED=true")
    print(f"PROVIDER={provider}")
    print(f"EVIDENCE_ID={evidence_id}")
    print(f"TRACE_ID={body['trace_id']}")
    print(f"EVIDENCE_STATUS={evidence.status_code}")
    print(f"TRACE_STATUS={trace.status_code}")
    print(f"WITNESS_STATUS={witness.status_code}")
    print(f"TRACEABILITY_STATUS={traceability.status_code}")
    print("AUTHORITY=human_gate_required")


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", action="store_true")
    args = parser.parse_args()

    if args.fixture:
        observe_output(
            "SHIRAKAMI_FIXTURE_PROVIDER_OBSERVATION",
            "fixture",
        )
        return

    token = os.getenv("COPILOT_GITHUB_TOKEN") or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token:
        print("LIVE_PROVIDER_OBSERVED=false")
        print("reason=provider credential not configured")
        return

    from copilot import CopilotClient

    copilot = CopilotClient()
    await copilot.start()
    try:
        session = await copilot.create_session()
        try:
            response = await session.send_and_wait(
                {"prompt": "Return exactly: SHIRAKAMI_LIVE_PROVIDER_OBSERVATION"}
            )
            content = getattr(getattr(response, "data", None), "content", None)
            if content is None:
                raise RuntimeError("Copilot SDK returned no assistant content")
            observe_output(content, "github-copilot-sdk")
            print("LIVE_PROVIDER_OBSERVED=true")
        finally:
            await session.destroy()
    finally:
        await copilot.stop()


if __name__ == "__main__":
    asyncio.run(main())
