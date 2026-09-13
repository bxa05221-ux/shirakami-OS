"""Activation-boundary check for the Shirakami Runtime.

This is deliberately a small control experiment. It checks the existing
entry boundaries without adding production behavior.
"""

from runtime.oppai_runtime_flow import prepare
from runtime.protocol_runtime_bridge import execute_protocol
from runtime.prototype import Transition


def local_adapter(prompt: str, protocol: str):
    return {"prompt": prompt, "protocol": protocol}


def main() -> int:
    text = "今日は少し引っかかっていることがある。"

    prepared = prepare(text)
    print("OPPAI_PREPARED", prepared.protocol, bool(prepared.input_for_runtime))

    # Control: the existing OPPAI flow requires the caller to supply the
    # adapter and protocol. This demonstrates the boundary, not a pump.
    adapted = local_adapter(prepared.input_for_runtime, prepared.protocol)
    print("OPPAI_ADAPTER", adapted["protocol"], bool(adapted["prompt"]))

    # Control: Runtime also requires the caller to supply Protocol IR and the
    # transition function. No human-text-to-Protocol selection is performed.
    protocol_ir = {"matome": {"title": "activation-boundary-control", "version": "0.1"}}

    def transition(_input):
        return Transition(kind="activation.control", data={"received": True})

    execution = execute_protocol(protocol_ir, transition, input_value={"text": text})
    print("RUNTIME_EXECUTED", execution.result.status, execution.result.steps)

    # This experiment intentionally does not manufacture a claim that these
    # three independently callable boundaries form one canonical path.
    print("ACTIVATION_BOUNDARY", "NOT_VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
