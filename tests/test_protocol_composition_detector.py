from pathlib import Path

from tools.protocol_composition_detector import compatibility_signal, detect


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


def test_compatibility_signal_is_structural_only(tmp_path: Path) -> None:
    source = tmp_path / "source.yaml"
    target = tmp_path / "target.yaml"

    source.write_text(
        """title: Source
version: v0.1
output:
  - context
""",
        encoding="utf-8",
    )
    target.write_text(
        """title: Target
version: v0.1
input:
  - context
""",
        encoding="utf-8",
    )

    result = compatibility_signal(detect(source), detect(target))

    assert result == {
        "structural_match": True,
        "matching_fields": ["context"],
        "semantic_compatibility": "unknown",
    }
