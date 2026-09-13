"""One-shot real-model observation through the existing activation path.

This experiment deliberately keeps model output opaque. It verifies only that a
secret-bearing execution environment can carry one request through:

human input -> Protocol Registry -> Protocol IR -> Runtime -> RealModelAdapter

No semantic interpretation, model-quality judgment, or automatic protocol
selection is performed here.
"""

import json

from experiments.openai_responses_transport import build_adapter
from runtime.activation_pump import activate
from runtime.protocol_loader import parse_matome
from runtime.protocol_registry import ProtocolRegistry
from runtime.prototype import Transition


MATOME = """matome:
  title: "Real Model Observation"
  version: "0.1"
  statement: >
    Observe one external model response without adding semantic interpretation.
  pipeline:
    - phase: "observation"
      action: "observe"
"""


INPUT_TEXT = "Observe this input without adding semantic interpretation."


def transition(input_value):
    return Transition(
        kind="real-model-observation",
        data={"text": input_value.get("text", ""), "changed": True},
    )


def main() -> int:
    artifact = parse_matome(MATOME)
    registry = ProtocolRegistry()
    registry.register_temporary(artifact.protocol_id, artifact, state="active")

    result = activate(
        INPUT_TEXT,
        registry=registry,
        protocol_id=artifact.protocol_id,
        transition=transition,
        ai_adapter=build_adapter(),
    )

    observation = {
        "protocol_id": result.protocol_id,
        "protocol_version": result.protocol_version,
        "runtime_status": result.runtime_result.status,
        "transition_kind": result.runtime_result.transition.kind,
        "evidence_confidence": result.evidence.confidence,
        "model_output": result.ai_output,
    }
    print(json.dumps(observation, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
