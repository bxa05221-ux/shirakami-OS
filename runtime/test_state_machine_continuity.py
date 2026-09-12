from runtime.evidence import capture_evidence
from runtime.i_field import IField, ImaginaryTerm
from runtime.landscape import LandscapeState
from runtime.landscape_execution import execute_on_landscape
from runtime.oppai_schema import normalize
from runtime.protocol_api import build_protocol_request, invoke_protocol
from runtime.protocol_registry import ProtocolRegistry
from runtime.prototype import Runtime, Transition
from runtime.replay import evidence_fingerprint


def test_state_machine_continuity_oppai_i_protocol_runtime_evidence_landscape():
    """Verify one observable continuity path without adding semantic ownership."""
    raw_input = "この件、何を先に確認すればいい？"
    observation = normalize(raw_input)
    field = IField((ImaginaryTerm("i-001", "left", observation.unresolved[0]),))
    assert field.unresolved_count() == 1

    runtime = Runtime()
    observed = runtime.execute(
        "oppai.observation",
        lambda context: Transition(kind="oppai.observation.recorded", data={"changed": True, "raw_input": context.input["raw_input"], "unresolved": context.input["unresolved"]}),
        {"raw_input": observation.raw_input, "unresolved": list(observation.unresolved)},
    )
    evidence_1 = capture_evidence(observed)
    evidence_1_ref = evidence_fingerprint(evidence_1)
    resolved = field.resolve("i-001", raw_input, evidence_1_ref)
    assert resolved.evidence_ref == evidence_1_ref

    registry = ProtocolRegistry()
    registry.register("continuity-e2e", {"version": "0.1", "title": "Continuity E2E"}, state="experimental")
    request = build_protocol_request(registry, "continuity-e2e", {"raw_input": raw_input, "resolved_i": resolved.value, "evidence_ref": resolved.evidence_ref})

    def adapter(protocol_request):
        return Runtime().execute(
            protocol_request.protocol_id,
            lambda context: Transition(kind="continuity.execution.completed", data={"changed": True, "raw_input": context.input["raw_input"], "resolved_i": context.input["resolved_i"], "evidence_ref": context.input["evidence_ref"]}),
            protocol_request.input,
        )

    result = invoke_protocol(request, adapter)
    evidence_2 = capture_evidence(result)
    assert evidence_2.transition_data["evidence_ref"] == evidence_1_ref
    assert evidence_2.transition_data["resolved_i"] == raw_input

    state = LandscapeState()
    landscape_evidence = execute_on_landscape(
        state,
        Runtime(),
        "landscape.continuity",
        lambda context: Transition(kind="landscape.continuity.observed", data={"changed": True, "evidence_ref": context.input["evidence_ref"], "resolved_i": context.input["resolved_i"]}),
        {"evidence_ref": evidence_2.transition_data["evidence_ref"], "resolved_i": evidence_2.transition_data["resolved_i"]},
    )
    assert landscape_evidence.transition_data["evidence_ref"] == evidence_1_ref
    assert landscape_evidence.transition_data["resolved_i"] == raw_input
