import pytest

from runtime.activated_cycle import ActivatedCycleError, execute_activated_cycle
from runtime.activation import ActivationResult
from runtime.evolution_bridge import ContextSnapshot
from runtime.evolution_pipeline import EvidenceDrivenRuntime
from runtime.prototype import Transition


def _ready_runtime(protocol_id="protocol-1"):
    runtime = EvidenceDrivenRuntime()
    runtime.observe(
        {"source": "test"},
        ContextSnapshot(protocol_id=protocol_id),
    )
    runtime.analyze(protocol_id, protocol_exists=False, diff_ref=protocol_id)
    assert runtime.approve(approved=True, reviewer="human")
    return runtime


def test_activated_cycle_requires_activation():
    runtime = _ready_runtime()
    activation = ActivationResult("protocol-1", "prepared", {})

    with pytest.raises(
        ActivatedCycleError,
        match="activated Protocol",
    ):
        execute_activated_cycle(
            activation,
            runtime,
            lambda context: Transition(
                kind="protocol-1",
                data={"ok": True},
            ),
        )


def test_activated_cycle_reaches_verification_and_evidence():
    runtime = _ready_runtime()
    activation = ActivationResult(
        "protocol-1",
        "activated",
        {"source": "human-gate"},
    )

    execution, verification = execute_activated_cycle(
        activation,
        runtime,
        lambda context: Transition(
            kind="protocol-1",
            data={"source": context.input["source"]},
        ),
        expected_transition_kind="protocol-1",
    )

    assert execution.status == "completed"
    assert execution.protocol_id == "protocol-1"
    assert verification.status == "pass"

    evidence = runtime.store.by_protocol("protocol-1")
    assert evidence
    assert any(
        record.transition_kind == "protocol-1"
        for record in evidence
    )


def test_activated_cycle_records_mismatch_as_evidence():
    runtime = _ready_runtime()
    activation = ActivationResult("protocol-1", "activated", {})

    execution, verification = execute_activated_cycle(
        activation,
        runtime,
        lambda context: Transition(
            kind="unexpected.transition",
            data={},
        ),
        expected_transition_kind="protocol-1",
    )

    assert execution.status == "completed"
    assert verification.status == "mismatch"

    evidence = runtime.store.by_protocol("protocol-1")
    assert any(
        record.transition_kind == "R0100:mismatch"
        for record in evidence
    )
