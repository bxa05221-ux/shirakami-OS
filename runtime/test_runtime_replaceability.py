from typing import Any, Mapping

from evolution_bridge import ContextSnapshot, ProtocolCandidate
from evolution_pipeline import EvidenceDrivenRuntime
from prototype import ExecutionContext, Runtime, Transition


class AlternateRuntime:
    """Minimal alternate implementation of the Runtime execution boundary."""

    def execute(
        self,
        protocol_id: str,
        protocol,
        input_data: Mapping[str, Any] | None = None,
    ):
        context = ExecutionContext(protocol_id=protocol_id, input=dict(input_data or {}))
        transition = protocol(context)
        return type("AlternateExecutionResult", (), {
            "status": "completed",
            "protocol_id": protocol_id,
            "transition": transition,
            "signals": ("transition.observed",),
            "steps": 1,
        })()


def _protocol(context: ExecutionContext) -> Transition:
    return Transition(kind="test.transition", data={"protocol_id": context.protocol_id})


def test_runtime_is_replaceable_without_granting_authority():
    candidate = ProtocolCandidate(
        protocol_id="P-REPLACE",
        diff_ref="D-001",
        rationale="Runtime independence test",
        source_evidence=("E-001",),
    )
    context = ContextSnapshot(
        landscape={"place": "test"},
        protocol_id=candidate.protocol_id,
        runtime_state="READY",
        metadata={"human_gate_required": True},
    )

    default_runtime = Runtime().execute(candidate.protocol_id, _protocol)
    alternate_runtime = AlternateRuntime().execute(candidate.protocol_id, _protocol)

    assert default_runtime.protocol_id == alternate_runtime.protocol_id == candidate.protocol_id
    assert default_runtime.transition.kind == alternate_runtime.transition.kind
    assert default_runtime.status == alternate_runtime.status == "completed"

    # Runtime implementation choice does not alter Core authority semantics.
    assert getattr(candidate, "authority", False) is False
    assert getattr(candidate, "executable", False) is False
    assert context.metadata["human_gate_required"] is True
    assert not getattr(default_runtime, "authority_granted", False)
    assert not getattr(alternate_runtime, "authority_granted", False)
    assert not getattr(default_runtime, "decision_authorized", False)
    assert not getattr(alternate_runtime, "decision_authorized", False)


def test_evidence_driven_runtime_accepts_replaceable_runtime_boundary():
    default = EvidenceDrivenRuntime(runtime=Runtime())
    alternate = EvidenceDrivenRuntime(runtime=AlternateRuntime())

    # The composition boundary accepts a Runtime implementation as a dependency.
    assert type(default.runtime) is Runtime
    assert type(alternate.runtime) is AlternateRuntime
