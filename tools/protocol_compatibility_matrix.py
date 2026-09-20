"""Build a structural Protocol compatibility matrix.

The matrix is intentionally conservative:
- structural field overlap is reported;
- semantic compatibility remains "unknown";
- no Runtime or Registry behavior is changed.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from tools.protocol_composition_detector import compatibility_signal, detect


def build_matrix(paths: list[Path]) -> list[dict[str, object]]:
    detected = [detect(path) for path in paths]
    matrix: list[dict[str, object]] = []
    for source in detected:
        for target in detected:
            if source["file"] == target["file"]:
                continue
            signal = compatibility_signal(source, target)
            matrix.append(
                {
                    "source": source["file"],
                    "target": target["file"],
                    **signal,
                }
            )
    return matrix


def render_markdown(matrix: list[dict[str, object]]) -> str:
    lines = [
        "# Protocol Compatibility Matrix",
        "",
        "Structural compatibility candidates only. Semantic compatibility is never inferred here.",
        "",
        "| Source | Target | Structural match | Matching fields | Semantic compatibility |",
        "|---|---|---:|---|---|",
    ]
    for item in matrix:
        fields = ", ".join(item["matching_fields"]) or "-"
        lines.append(
            f'| `{item["source"]}` | `{item["target"]}` | '
            f'{str(item["structural_match"]).lower()} | {fields} | '
            f'{item["semantic_compatibility"]} |'
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root)
    paths = sorted((root / "protocols").rglob("*.yaml"))
    print(render_markdown(build_matrix(paths)), end="")


if __name__ == "__main__":
    main()
