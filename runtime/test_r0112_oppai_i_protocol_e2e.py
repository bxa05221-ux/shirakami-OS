from runtime.evidence import capture_evidence
from runtime.i_field import IField, ImaginaryTerm
from runtime.oppai_schema import normalize
from runtime.protocol_api import build_protocol_request, invoke_protocol
from runtime.protocol_registry import ProtocolRegistry
from runtime.prototype import Runtime, Transition
from runtime.replay import evidence_fingerprint


def test_r0112_oppai_i_protocol_runtime_adapter_evidence_path():
    """Verify the compositional UI-for-AI path without adding semantic ownership."""
    raw_input = "この件、何を先に確認すればいい？"

    # 1. Natural human input enters through the OPPAI observation boundary.
    observation = normalize(raw_input)
    assert observation.raw_input == raw_input
    assert observation.canonical_prompt == raw_input
    assert observation.unresolved == (raw_input,)

    # 2. The unresolved observation is held as an i-term; no interpretation is inferred.
    field = IField(
        (
            ImaginaryTerm(
                "i-001",
                "left",
                observation.unresolved[0],
            ),
        )
    )
    assert field.unresolved_count() == 1

    # 3. An observable Runtime transition supplies the Evidence reference.
    runtime = Runtime()
    observed = runtime.execute(
        "oppai.observation",
        lambda context: Transition(
            kind="oppai.observation.recorded",
            data={
                "changed": True,
                "raw_input": context.input["raw_input"],
                "unresolved": context.input["unresolved"],
            },
        ),
        {
            "raw_input": observation.raw_input,
            "unresolved": list(observation.unresolved),
        },
    )
    evidence_1 = capture_evidence(observed)
    evidence_ref = evidence_fingerprint(evidence_1)

    assert evidence_1.protocol_id == "oppai.observation"
    assert evidence_1.transition_data["raw_input"] == raw_input
    assert "interpretation" not in evidence_1.transition_data

    # 4. i is resolved only with the observed Evidence reference.
    resolved = field.resolve(
        "i-001",
        evidence_1.transition_data["unresolved"][0],
        evidence_ref,
    )
    assert resolved.evidence_ref == evidence_ref
    assert field.unresolved_count() == 0

    # 5. Protocol selection is owned by the canonical Registry/API boundary.
    registry = ProtocolRegistry()
    registry.register(
        "r0112-e2e",
        {"version": "0.1", "title": "R0112 E2E"},
        state="experimental",
    )
    request = build_protocol_request(
        registry,
        "r0112-e2e",
        {
            "raw_input": observation.raw_input,
            "resolved_i": resolved.value,
            "evidence_ref": resolved.evidence_ref,
        },
    )
    assert request.protocol_id == "r0112-e2e"
    assert request.input["raw_input"] == raw_input
    assert request.input["evidence_ref"] == evidence_ref

    # 6. Runtime invokes a replaceable Adapter callable through the ProtocolRequest boundary.
    adapter_calls = []

    def adapter(protocol_request):
        adapter_calls.append(protocol_request.protocol_id)
        return Runtime().execute(
            protocol_request.protocol_id,
            lambda context: Transition(
                kind="adapter.execution.completed",
                data={
                    "changed": True,
                    "raw_input": context.input["raw_input"],
                    "resolved_i": context.input["resolved_i"],
                    "evidence_ref": context.input["evidence_ref"],
                },
            ),
            protocol_request.input,
        )

    result = invoke_protocol(request, adapter)
    evidence_2 = capture_evidence(result)

    # 7. The Runtime-produced Evidence remains the observable result boundary.
    assert adapter_calls == ["r0112-e2e"]
    assert result.status == "completed"
    assert evidence_2.protocol_id == "r0112-e2e"
    assert evidence_2.transition_kind == "adapter.execution.completed"
    assert evidence_2.transition_data["raw_input"] == raw_input
    assert evidence_2.transition_data["evidence_ref"] == evidence_ref
    assert "interpretation" not in evidence_2.transition_data

    # 8. No UI-layer interpretation is promoted into Protocol semantics.
    assert request.protocol_id == "r0112-e2e"
    assert request.input["resolved_i"] == raw_input
