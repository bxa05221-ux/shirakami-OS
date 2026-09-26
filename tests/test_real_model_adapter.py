from runtime.activation_pump import activate
from runtime.protocol_loader import parse_matome
from runtime.protocol_registry import ProtocolRegistry
from runtime.prototype import Transition
from runtime.real_model_adapter import ModelRequest, RealModelAdapter


def test_real_model_adapter_passes_canonical_prompt_and_context():
    observed = {}

    def transport(request: ModelRequest):
        observed["request"] = request
        return {"output": "model-observed"}

    adapter = RealModelAdapter(transport)
    result = adapter("canonical input", "test.protocol")

    assert result == {"output": "model-observed"}
    assert observed["request"].canonical_prompt == "canonical input"
    assert observed["request"].context == {"protocol_id": "test.protocol"}


def test_activation_pump_links_model_output_into_evidence():
    matome = """matome:
  title: "Keyless Model Observation"
  version: "0.1"
  statement: >
    Observe one external model response without semantic interpretation.
  pipeline:
    - phase: "observation"
      action: "observe"
"""
    artifact = parse_matome(matome)
    registry = ProtocolRegistry()
    registry.register_temporary(artifact.protocol_id, artifact, state="active")

    def transition(input_value):
        return Transition(
            kind="model-observation",
            data={"text": input_value.get("text", ""), "changed": True},
        )

    adapter = RealModelAdapter(
        lambda request: {
            "output": "keyless-model-response",
            "protocol_id": request.context["protocol_id"],
        }
    )

    result = activate(
        "Observe this input.",
        registry=registry,
        protocol_id=artifact.protocol_id,
        transition=transition,
        ai_adapter=adapter,
    )

    assert result.ai_output["output"] == "keyless-model-response"
    assert result.evidence.model_output == result.ai_output
    assert result.evidence.protocol_id == result.protocol_id
    assert result.evidence.transition_kind == "model-observation"
