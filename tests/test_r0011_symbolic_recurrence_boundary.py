from pathlib import Path

from runtime.evidence import capture_evidence
from runtime.protocol_loader import load_matome
from runtime.prototype import Runtime, Transition


FIXTURE = Path(__file__).parents[1] / "protocols" / "manual" / "symbolic-recurrence-boundary.yaml"


def test_r0011_symbolic_recurrence_crosses_runtime_boundary_without_semantic_interpretation():
    protocol_ir = load_matome(FIXTURE)

    def boundary_protocol(context):
        return Transition(
            kind="symbolic.recurrence.observed",
            data={
                "changed": True,
                "protocol_id": context.protocol_id,
                "title": protocol_ir.title,
                "version": protocol_ir.version,
                "statement": protocol_ir.statement,
                "pipeline": tuple(dict(item) for item in protocol_ir.pipeline),
            },
        )

    runtime = Runtime()
    result = runtime.execute(protocol_ir.protocol_id, boundary_protocol, {})
    evidence = capture_evidence(result)

    assert protocol_ir.protocol_id == "symbolic.recurrence.boundary.test"
    assert [item["action"] for item in protocol_ir.pipeline] == [
        "preserve_symbolic_lineage",
        "carry_symbolic_reference_as_protocol_data",
        "expose_recurrence_as_observable_transition",
        "preserve_recurrence_lineage",
    ]
    assert result.status == "completed"
    assert result.transition.kind == "symbolic.recurrence.observed"
    assert result.transition.data["pipeline"] == protocol_ir.pipeline
    assert evidence.transition_kind == "symbolic.recurrence.observed"
    assert evidence.transition_data["statement"] == protocol_ir.statement
    assert evidence.transition_data["pipeline"] == protocol_ir.pipeline
