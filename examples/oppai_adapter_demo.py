"""Runnable OPPAI adapter demonstration.

This example deliberately uses a local deterministic adapter so the complete
boundary can be exercised without API credentials. Replace `local_adapter`
with a real model adapter at the same callable boundary.
"""

from runtime.oppai_runtime_flow import run_oppai_flow


def local_adapter(prompt: str, context: dict) -> dict:
    return {
        "adapter": "local-demo",
        "received_prompt": prompt,
        "received_context": context,
    }


if __name__ == "__main__":
    result = run_oppai_flow(
        "ちょっと待って。いや、そこじゃない。さっきの話を続けたい。",
        adapter=local_adapter,
        context={"thread": "demo-001"},
    )
    print(result)
