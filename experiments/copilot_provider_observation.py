"""Minimal live Copilot provider observation harness.

Authentication is supplied only by the provider environment. The harness does
not persist credentials or treat model output as authority.
"""
from __future__ import annotations
import asyncio
import os
from copilot import CopilotClient

PROMPT = "Return exactly: SHIRAKAMI_LIVE_PROVIDER_OBSERVATION"

async def main() -> None:
    if not (os.getenv("COPILOT_GITHUB_TOKEN") or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")):
        print("LIVE_PROVIDER_OBSERVED=false")
        print("reason=provider credential not configured")
        return

    client = CopilotClient()
    await client.start()
    try:
        session = await client.create_session()
        try:
            response = await session.send_and_wait({"prompt": PROMPT})
            content = getattr(getattr(response, "data", None), "content", None)
            if content is None:
                raise RuntimeError("Copilot SDK returned no assistant content")
            print("LIVE_PROVIDER_OBSERVED=true")
            print(f"MODEL_OUTPUT={content}")
            print("AUTHORITY=human_gate_required")
        finally:
            await session.destroy()
    finally:
        await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
