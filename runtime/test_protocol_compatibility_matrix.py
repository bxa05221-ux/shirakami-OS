from pathlib import Path

from tools.protocol_compatibility_matrix import build_matrix


def _write(path: Path, title: str, input_name: str, output_name: str) -> None:
    path.write_text(
        f"""title: {title}
version: v0.1
input:
  - {input_name}
output:
  - {output_name}
flow:
  - observe
  - verify
""",
        encoding="utf-8",
    )


def test_matrix_reports_structural_match_and_unknown_semantics(tmp_path: Path) -> None:
    source = tmp_path / "source.yaml"
    target = tmp_path / "target.yaml"
    _write(source, "Source", "input", "context")
    _write(target, "Target", "context", "evidence")

    matrix = build_matrix([source, target])

    forward = next(item for item in matrix if item["source"] == str(source) and item["target"] == str(target))
    reverse = next(item for item in matrix if item["source"] == str(target) and item["target"] == str(source))

    assert forward["structural_match"] is True
    assert forward["matching_fields"] == ["context"]
    assert forward["semantic_compatibility"] == "unknown"
    assert reverse["structural_match"] is False
    assert reverse["semantic_compatibility"] == "unknown"