"""Verify one explicit OPPAI -> Protocol Registry -> Runtime -> AI path."""

from runtime.activation_pump import activate
from runtime.protocol_loader import parse_matome
from runtime.protocol_registry import ProtocolRegistry
from runtime.prototype import Transition


class TestAI:
    def __call__(self, prompt: str, protocol_id: str) -> dict[str, str]:
        return {"protocol": protocol_id, "prompt": prompt, "status": "received"}


def transition(input_value):
    return Transition(kind="activation", data={"text": input_value.get("text", "")})


def main() -> None:
    artifact = parse_matome(
        '''matome:
  title: "Activation Pump Test"
  version: "0.1"
  statement: >
    Test-only protocol for the activation boundary.
  pipeline:
    - phase: "test"
      action: "activate"
'''
    )
    registry = ProtocolRegistry()
    registry.register_temporary(artifact.protocol_id, artifact, state="active")

    result = activate(
        "今日は少し引っかかっていることがある。",
        registry=registry,
        protocol_id=artifact.protocol_id,
        transition=transition,
        ai_adapter=TestAI(),
    )

    assert result.protocol_id == artifact.protocol_id
    assert result.protocol_version == artifact.version
    assert result.runtime_result.transition.kind == "activation"
    assert result.ai_output["protocol"] == artifact.protocol_id
    print("ACTIVATION_PUMP VERIFIED")


if __name__ == "__main__":
    main()
