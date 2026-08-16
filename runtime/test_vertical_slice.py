"""Integration test for the complete β0.1 Matome vertical slice."""

from pathlib import Path

from vertical_slice import execute_matome


PROTOCOL = Path(__file__).resolve().parents[1] / "protocols" / "manual" / "manga-user-manual.yaml"


def test_matome_to_evidence_to_landscape_vertical_slice():
    result = execute_matome(PROTOCOL, {"language": "ja"})

    assert result.protocol.title == "Shirakami OS User Manual Manga"
    assert result.protocol.version == "0.1"

    assert result.execution.status == "completed"
    assert result.execution.protocol_id == result.protocol.protocol_id
    assert result.execution.transition.kind == "matome.protocol.transition"
    assert result.execution.transition.data["changed"] is True

    assert result.evidence.protocol_id == result.execution.protocol_id
    assert result.evidence.status == "completed"
    assert result.evidence.transition_kind == "matome.protocol.transition"
    assert result.evidence.transition_data["changed"] is True

    assert result.landscape["protocol_id"] == result.protocol.protocol_id
    assert result.landscape["protocol_title"] == result.protocol.title
    assert result.landscape["protocol_version"] == result.protocol.version
    assert result.landscape["input"] == {"language": "ja"}
    assert result.landscape["changed"] is True
