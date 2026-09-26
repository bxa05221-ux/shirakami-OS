"""Minimal live-provider observation harness.

The harness is intentionally small: it obtains one provider response and
routes that output through the existing Shirakami HTTP execution boundary.
Credentials are read from the environment and never persisted.
"""
from __future__ import annotations

import asyncio
import os

from fastapi.testclient import TestClient

from api.http import ShirakamiHTTPTransport
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


async def main() -> None:
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

            transport = ShirakamiHTTPTransport(
                protocol_registry={PROTOCOL_ID: protocol},
                api_key=API_KEY,
                model_adapter=lambda _prompt, _protocol_id: {
                    "output": content,
                    "provider": "github-copilot-sdk",
                },
            )
            http = TestClient(transport.create_app())
            payload = {
                "protocol_id": PROTOCOL_ID,
                "input_data": {
                    "text": "live copilot observation",
                    "provider_output": content,
                },
                "handoff_id": HANDOFF_ID,
                "trace_id": TRACE_ID,
                "evidence_ids": [],
                "boundary_context": {
                    "handoff_id": HANDOFF_ID,
                    "project": "Shirakami API MVP",
                    "objective": "Observe real Copilot output through the Shirakami evidence boundary",
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
            print("LIVE_PROVIDER_OBSERVED=true")
            print(f"EVIDENCE_ID={evidence_id}")
            print(f"TRACE_ID={body['trace_id']}")
            print(f"EVIDENCE_STATUS={evidence.status_code}")
            print(f"TRACE_STATUS={trace.status_code}")
            print(f"WITNESS_STATUS={witness.status_code}")
            print("AUTHORITY=human_gate_required")
        finally:
            await session.destroy()
    finally:
        await copilot.stop()


if __name__ == "__main__":
    asyncio.run(main())
