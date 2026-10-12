"""Run one live OpenAI Responses call through Shirakami HTTP and verify its trace."""
from __future__ import annotations
import asyncio, os, sys, uuid
from pathlib import Path
from typing import Any
import httpx
ROOT = str(Path(__file__).resolve().parents[1])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from fastapi.testclient import TestClient
from api.http import ShirakamiHTTPTransport
from runtime.api import ShirakamiAPI
from runtime.prototype import Transition

API_KEY = "local-openai-http-observation-key"
PROTOCOL_ID = "openai.http.observation"
HANDOFF_ID = "SH-HO-OPENAI-HTTP-001"
RESPONSES_URL = os.getenv("OPENAI_RESPONSES_URL", "https://api.openai.com/v1/responses")

def observation_protocol(context: Any) -> Transition:
    return Transition(kind=PROTOCOL_ID, data={
        "provider_output_received": context.input.get("provider_output") is not None,
    })

async def openai_provider_adapter(prompt: str, protocol_id: str) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "").strip()
    if not api_key or not model:
        raise RuntimeError("OPENAI_API_KEY and OPENAI_MODEL are required")
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            RESPONSES_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": model, "input": prompt},
        )
        response.raise_for_status()
        payload = response.json()
    if payload.get("status") != "completed":
        raise AssertionError(f"OpenAI response did not complete: {payload.get('status')!r}")
    chunks = [
        part["text"]
        for item in payload.get("output", []) if isinstance(item, dict)
        for part in item.get("content", [])
        if isinstance(part, dict) and part.get("type") == "output_text"
        and isinstance(part.get("text"), str) and part["text"]
    ]
    output = "\n".join(chunks).strip()
    if not output:
        raise AssertionError("OpenAI Responses API returned no output_text")
    # Never copy the full response or encrypted reasoning payload into evidence.
    return {
        "output": output, "provider": "openai", "model": model,
        "protocol_id": protocol_id, "response_id": payload.get("id"),
        "provider_status": payload.get("status"),
    }

def assert_boundary(client: TestClient, body: dict[str, Any], trace_id: str) -> None:
    evidence_ids = body.get("evidence_ids") or []
    if len(evidence_ids) != 1:
        raise AssertionError(f"expected one linked Evidence ID; got {evidence_ids!r}")
    evidence_id = evidence_ids[0]
    headers = {"X-API-Key": API_KEY}
    responses = [
        client.get(f"/v1/evidence/{evidence_id}", headers=headers),
        client.get(f"/v1/traces/{trace_id}", headers=headers),
        client.get(f"/v1/witnesses/{trace_id}", headers=headers),
        client.get(f"/v1/traceability/{trace_id}", headers=headers),
    ]
    for response in responses:
        response.raise_for_status()
    evidence, trace, witness, traceability = [response.json() for response in responses]
    if evidence.get("model_output") != body.get("model_output"):
        raise AssertionError("HTTP model output does not match stored Evidence")
    for name, record in (("Trace", trace), ("AIwitness", witness)):
        if record.get("evidence_ids") != [evidence_id]:
            raise AssertionError(f"{name} does not reference the exact Evidence ID")
        if record.get("verification_status") != "pass":
            raise AssertionError(f"{name} does not preserve passing verification")
    if traceability.get("valid") is not True:
        raise AssertionError("traceability verification did not return valid=true")
    for flag in ("execution_authorized", "publish_authorized", "merge_authorized"):
        if body.get(flag) is not False:
            raise AssertionError(f"{flag} must remain false")
    if body.get("human_gate_required") is not True:
        raise AssertionError("human_gate_required must remain true")
    print("BOUNDARY_OBSERVED=true")
    print("PROVIDER=openai")
    print(f"EVIDENCE_ID={evidence_id}")
    print(f"TRACE_ID={trace_id}")
    print("AUTHORITY=human_gate_required")
    print("TRACEABILITY_VALID=true")

async def main() -> None:
    if not os.getenv("OPENAI_API_KEY", "").strip() or not os.getenv("OPENAI_MODEL", "").strip():
        raise SystemExit("Missing OPENAI_API_KEY or OPENAI_MODEL; fixture fallback is disabled")
    trace_id = f"TRACE-OPENAI-HTTP-{uuid.uuid4().hex[:12]}"
    transport = ShirakamiHTTPTransport(
        api=ShirakamiAPI(),
        protocol_registry={PROTOCOL_ID: observation_protocol},
        api_key=API_KEY,
        async_model_adapter=openai_provider_adapter,
    )
    client = TestClient(transport.create_app())
    headers = {"X-API-Key": API_KEY}
    observe = client.post("/v1/observe", headers=headers, json={
        "observation": {"signal": "execute"},
        "context": {"protocol_id": PROTOCOL_ID, "landscape": {},
                    "metadata": {"source": "openai-http-observation"}},
        "handoff_id": HANDOFF_ID, "trace_id": trace_id, "evidence_ids": [],
    })
    observe.raise_for_status()
    analyze = client.post("/v1/analyze", headers=headers,
                          json={"protocol_id": PROTOCOL_ID, "protocol_exists": True})
    analyze.raise_for_status()
    # Harness approval exercises the explicit approval endpoint; this is not
    # production operator identity verification or an interactive approval UI.
    approve = client.post("/v1/approve", headers=headers, json={
        "approved": True, "reviewer": "contest-observation-harness",
        "human_authorized": True,
    })
    approve.raise_for_status()
    if approve.json().get("accepted") is not True:
        raise AssertionError(f"approval was not accepted: {approve.json()!r}")
    payload = {
        "protocol_id": PROTOCOL_ID,
        "input_data": {"text": "Observe this input without adding semantic interpretation."},
        "handoff_id": HANDOFF_ID, "trace_id": trace_id, "evidence_ids": [],
        "boundary_context": {
            "handoff_id": HANDOFF_ID, "project": "Shirakami API MVP",
            "objective": "Verify live OpenAI output through HTTP, Runtime, Evidence, Trace, and AIwitness",
            "protocol_ids": [PROTOCOL_ID], "evidence_ids": [],
            "verification_scope": ["HTTP", "OpenAI Responses API", "Runtime", "Evidence", "Trace", "AIwitness"],
            "execution_authorized": False, "publish_authorized": False,
            "merge_authorized": False, "human_gate_required": True,
        },
    }
    response = client.post("/v1/execute", headers=headers, json=payload)
    response.raise_for_status()
    body = response.json()
    output = body.get("model_output")
    if not isinstance(output, dict) or not isinstance(output.get("output"), str) or not output["output"].strip():
        raise AssertionError("HTTP execution returned no live provider output")
    if output.get("provider") != "openai" or output.get("provider_status") != "completed":
        raise AssertionError("output does not identify a completed OpenAI response")
    execution_id = body.get("execution_id")
    if not isinstance(execution_id, str) or not execution_id:
        raise AssertionError("HTTP execution did not return execution_id")
    verify = client.post(f"/v1/executions/{execution_id}/verify", headers=headers,
                         json={"expected_transition_kind": PROTOCOL_ID})
    verify.raise_for_status()
    if verify.json().get("status") != "pass":
        raise AssertionError(f"verification did not pass: {verify.json()!r}")
    assert_boundary(client, body, trace_id)
    print("VERIFICATION_STATUS=pass")
    print("LIVE_PROVIDER_OBSERVED=true")
    print("MODEL_OUTPUT_NONEMPTY=true")

if __name__ == "__main__":
    asyncio.run(main())
