"""Verify continuity across the complete explicit activation path.

This is a control experiment only. It does not add production semantics or
select a protocol automatically.
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
        return {"protocol_id": protocol_id, "status": "received"}


def transition(input_value):
    return Transition(
        kind="activation.e2e",
        data={"text": input_value.get("text", ""), "changed": True},
    )


def main() -> int:
    text = "同じ入力が最後まで同じ経路を通るか確認する。"
    artifact = parse_matome(
        '''matome:\n  title: "Activation E2E Continuity Test"\n  version: "0.1"\n  statement: >\n    Test-only protocol for end-to-end continuity.\n  pipeline:\n    - phase: "test"\n      action: "activate"\n'''
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

    assert result.protocol_id == artifact.protocol_id
    assert result.runtime_result.protocol_id == artifact.protocol_id
    assert result.runtime_result.transition.kind == "activation.e2e"
    assert result.runtime_result.transition.data["text"] == text
    assert result.evidence.protocol_id == artifact.protocol_id
    assert is_transition_evidence(result.evidence)
    assert ai.request["prompt"] == text
    assert ai.request["protocol_id"] == artifact.protocol_id
    assert result.ai_output["protocol_id"] == artifact.protocol_id

    print("INPUT", text)
    print("PROTOCOL_ID", artifact.protocol_id)
    print("RUNTIME", result.runtime_result.status)
    print("EVIDENCE", result.evidence.protocol_id)
    print("AI", result.ai_output["status"])
    print("ACTIVATION_E2E_CONTINUITY", "VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
