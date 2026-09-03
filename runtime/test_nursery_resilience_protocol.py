"""Executable boundary test for the nursery resilience protocol candidate."""

from pathlib import Path

from protocol_loader import load_matome


PROTOCOL = Path(__file__).parents[1] / "protocols" / "resilience" / "nursery-resilience.yaml"


def test_nursery_resilience_protocol_loads_and_preserves_cycle_boundary():
    protocol = load_matome(PROTOCOL)

    assert protocol.title == "Shirakami Nursery Resilience Protocol"
    assert protocol.version == "0.1"
    assert [step["phase"] for step in protocol.pipeline] == [
        "observe",
        "dialogue",
        "record",
        "share",
        "support",
        "growth",
        "reobserve",
        "evidence",
    ]


def test_nursery_resilience_pipeline_contains_no_decision_phase():
    protocol = load_matome(PROTOCOL)
    phases = {step["phase"] for step in protocol.pipeline}

    assert "diagnose" not in phases
    assert "decide" not in phases
