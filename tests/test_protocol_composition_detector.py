from pathlib import Path

from tools.protocol_composition_detector import detect


def test_detects_input_output_route_and_boundaries(tmp_path: Path) -> None:
    protocol = tmp_path / "sample.yaml"
    protocol.write_text(
        """title: Sample\nversion: v0.1\ninput:\n  - context\noutput:\n  - evidence\nflow:\n  - observe\n  - verify\n""",
        encoding="utf-8",
    )

    result = detect(protocol)

    assert result["title"] == "Sample"
    assert result["version"] == "v0.1"
    assert result["inputs"] == ["context"]
    assert result["outputs"] == ["evidence"]
    assert result["route"] == ["observe", "verify"]
    assert result["signals"] == {
        "has_input": True,
        "has_output": True,
        "has_route": True,
        "has_evidence": True,
        "has_landscape": False,
    }
