from pathlib import Path

from evidence import capture_evidence
from landscape import LandscapeState
from protocol_loader import load_matome
from protocol_runtime_bridge import execute_protocol
from prototype import Transition


def test_symbolic_recurrence_fixture_loads_and_preserves_pipeline():
    fixture = Path(__file__).parents[1] / "protocols" / "manual" / "symbolic-recurrence-boundary.yaml"
    protocol_ir = load_matome(fixture)

    assert protocol_ir.title == "Symbolic Recurrence Boundary Test"
    assert protocol_ir.version == "0.1"
    assert [item["phase"] for item in protocol_ir.pipeline] == [
        "observation",
        "recurrence",
        "transition",
        "evidence",
    ]
    assert [item["action"] for item in protocol_ir.pipeline] == [
        "preserve_symbolic_lineage",
        "carry_symbolic_reference_as_protocol_data",
        "expose_recurrence_as_observable_transition",
        "preserve_recurrence_lineage",
    ]


def test_symbolic_recurrence_lineage_survives_runtime_and_landscape_boundary():
    protocol = {
        "matome": {
            "title": "Symbolic Recurrence Boundary Test",
            "version": "0.1",
            "statement": "Preserve symbolic lineage without making Runtime own domain meaning.",
            "pipeline": [
                {"phase": "observation", "action": "preserve_symbolic_lineage"},
                {"phase": "recurrence", "action": "carry_symbolic_reference_as_protocol_data"},
                {"phase": "transition", "action": "expose_recurrence_as_observable_transition"},
                {"phase": "evidence", "action": "preserve_recurrence_lineage"},
            ],
        }
    }

    def transition(value):
        return Transition(
            kind="symbolic.recurrence",
            data={
                "changed": True,
                "symbolic_reference": "grandfather.said",
                "lineage": {
                    "source": "human.landscape",
                    "relation": "grandfather",
                    "recurrence": "current_context",
                },
                "input": value,
            },
        )

    execution = execute_protocol(
        protocol,
        transition,
        input_value={"context": "current-situation"},
    )

    evidence = capture_evidence(execution.result)
    landscape = LandscapeState.empty()
    landscape.apply_evidence(evidence)

    assert execution.protocol_title == "Symbolic Recurrence Boundary Test"
    assert execution.protocol_version == "0.1"
    assert execution.result.status == "completed"
    assert execution.result.transition.kind == "symbolic.recurrence"
    assert evidence.transition_kind == "symbolic.recurrence"
    assert evidence.transition_data["symbolic_reference"] == "grandfather.said"
    assert evidence.transition_data["lineage"]["relation"] == "grandfather"
    assert landscape.snapshot()["symbolic_reference"] == "grandfather.said"
    assert landscape.snapshot()["lineage"]["recurrence"] == "current_context"


def test_runtime_does_not_need_to_interpret_symbolic_identity():
    protocol = {
        "matome": {
            "title": "Symbolic Identity Neutrality Test",
            "version": "0.1",
        }
    }

    def transition(value):
        return Transition(
            kind="symbolic.reference",
            data={
                "changed": True,
                "reference": value["reference"],
            },
        )

    execution = execute_protocol(
        protocol,
        transition,
        input_value={"reference": "grandfather.said"},
    )

    assert execution.result.status == "completed"
    assert execution.result.transition.data == {
        "changed": True,
        "reference": "grandfather.said",
    }
