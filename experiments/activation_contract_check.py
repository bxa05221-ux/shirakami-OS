"""Verify the observable contract across the explicit activation path.

Control experiment only. This check protects boundary continuity without adding
production semantics or automatic protocol selection.
"""

from runtime.activation_pump import activate
from runtime.evidence import is_transition_evidence
from runtime.protocol_loader import parse_matome
from runtime.protocol_registry import ProtocolRegistry
from runtime.prototype import Transition


class ExternalAIStandIn:
    def __init__(self):
        self.request = None

    def __call__(self, prompt: str, protocol_id: str) -> dict[str, str]:
        self.request = {"prompt": prompt, "protocol_id": protocol_id}
        return {"protocol_id": protocol_id, "output": "observed"}


def transition(input_value):
    return Transition(
        kind="activation.contract",
        data={"text": input_value.get("text", ""), "changed": True},
    )


def main() -> int:
    text = "activation contract must preserve the same observable identity."
    artifact = parse_matome(
        '''matome:
  title: "Activation Contract Test"
  version: "0.1"
  statement: >
    Test-only protocol for activation boundary continuity.
  pipeline:
    - phase: "test"
      action: "activate"
'''
    )
    registry = ProtocolRegistry()
    registry.register_temporary(artifact.protocol_id, artifact, state="active")
    ai = ExternalAIStandIn()

    result = activate(
        text,
        registry=registry,
        protocol_id=artifact.protocol_id,
        transition=transition,
        ai_adapter=ai,
    )

    # Stable contract: identity and input remain observable at each boundary.
    assert result.protocol_id == artifact.protocol_id
    assert result.runtime_result.protocol_id == artifact.protocol_id
    assert result.evidence.protocol_id == artifact.protocol_id
    assert ai.request["protocol_id"] == artifact.protocol_id
    assert ai.request["prompt"] == text
    assert result.runtime_result.transition.data["text"] == text
    assert result.runtime_result.transition.kind == "activation.contract"
    assert is_transition_evidence(result.evidence)

    # Contract does not assert semantic meaning or authority.
    assert result.evidence.confidence == "observed"

    print("ACTIVATION_CONTRACT VERIFIED")
    print("PROTOCOL_ID", result.protocol_id)
    print("INPUT_PRESERVED", ai.request["prompt"] == text)
    print("IDENTITY_PRESERVED", result.protocol_id == result.evidence.protocol_id)
    print("EVIDENCE_CONFIDENCE", result.evidence.confidence)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
