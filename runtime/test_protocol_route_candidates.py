from pathlib import Path

import pytest

from tools.protocol_route_candidates import generate_candidates


def _write(path: Path, input_name: str, output_name: str) -> None:
    path.write_text(
        f"""title: {path.stem}
version: v0.1
input:
  - {input_name}
output:
  - {output_name}
""",
        encoding="utf-8",
    )


def test_generates_ordered_three_gram_without_reusing_protocol(tmp_path: Path) -> None:
    a = tmp_path / "a.yaml"
    b = tmp_path / "b.yaml"
    c = tmp_path / "c.yaml"
    d = tmp_path / "d.yaml"
    _write(a, "seed", "context")
    _write(b, "context", "evidence")
    _write(c, "evidence", "decision")
    _write(d, "other", "unrelated")

    candidates = generate_candidates([a, b, c, d], 3)

    assert (str(a), str(b), str(c)) in candidates
    assert all(len(route) == 3 for route in candidates)
    assert all(len(set(route)) == 3 for route in candidates)


def test_rejects_zero_or_one_gram(tmp_path: Path) -> None:
    a = tmp_path / "a.yaml"
    b = tmp_path / "b.yaml"
    _write(a, "seed", "context")
    _write(b, "context", "evidence")

    with pytest.raises(ValueError):
        generate_candidates([a, b], 1)
