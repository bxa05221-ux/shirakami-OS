from pathlib import Path

from runtime.vertical_slice import execute_matome


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "protocols" / "research" / "anmon-layer-reverse.yaml"


def test_r0012_execute_matome_reaches_evidence_and_landscape():
    result = execute_matome(
        FIXTURE,
        {
            "source_landscape_state": "landscape-r0012-001",
            "observation": {"note": "source observable landscape"},
        },
    )

    assert result.protocol.protocol_id == "matome.protocol"
    assert result.protocol.title == "暗問層逆算プロトコル"
    assert result.execution.status == "completed"
    assert result.evidence.protocol_id == "matome.protocol"
    assert result.evidence.transition_kind == "matome.protocol.transition"
    assert result.evidence.transition_data["input"]["source_landscape_state"] == "landscape-r0012-001"
    assert result.landscape["input"]["source_landscape_state"] == "landscape-r0012-001"


def test_r0012_vertical_slice_keeps_lineage_as_observable_data():
    result = execute_matome(
        FIXTURE,
        {"source_landscape_state": "landscape-r0012-001"},
    )

    transition_data = result.evidence.transition_data
    assert transition_data["protocol_id"] == "matome.protocol"
    assert transition_data["changed"] is True
    assert "continuity" not in result.landscape
    assert "continuity_claim" not in result.landscape
