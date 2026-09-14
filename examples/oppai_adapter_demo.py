"""Runnable OPPAI adapter demonstration.

This example deliberately uses a local deterministic adapter so the complete
boundary can be exercised without API credentials. Replace `local_adapter`
with a real model adapter at the same callable boundary.
"""

from runtime.oppai_runtime_flow import execute


def local_adapter(prompt: str, protocol: str) -> dict:
    return {
        "adapter": "local-demo",
        "received_prompt": prompt,
        "received_protocol": protocol,
    }


if __name__ == "__main__":
    result = execute(
        "ちょっと待って。いや、そこじゃない。さっきの話を続けたい。",
        runtime_adapter=local_adapter,
        protocol="default",
        context={"thread": "demo-001"},
    )
    print(result)
