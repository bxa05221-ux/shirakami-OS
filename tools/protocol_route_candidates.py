"""Generate conservative n-gram Protocol route candidates.

An n-gram is an ordered sequence of distinct Protocol artifacts where every
adjacent pair has a structural compatibility signal. This module does not
infer semantic compatibility and does not execute or authorize routes.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from collections.abc import Iterable

try:
    from runtime.evidence import EvidenceRecord
except ImportError:
    from evidence import EvidenceRecord

from tools.protocol_compatibility_matrix import build_matrix


def generate_candidates(
    paths: list[Path],
    n: int,
) -> list[tuple[str, ...]]:
    """Return simple directed paths of exactly n Protocol artifacts."""
    if n < 2:
        raise ValueError("n must be >= 2")

    matrix = build_matrix(paths)
    edges = {
        (item["source"], item["target"])
        for item in matrix
        if item["structural_match"] is True
    }
    nodes = sorted({str(path) for path in paths})
    candidates: list[tuple[str, ...]] = []

    def extend(route: tuple[str, ...]) -> None:
        if len(route) == n:
            candidates.append(route)
            return
        source = route[-1]
        for target in nodes:
            if target in route:
                continue
            if (source, target) in edges:
                extend(route + (target,))

    for node in nodes:
        extend((node,))

    return candidates


def generate_candidates_from_evidence(
    evidence: Iterable[EvidenceRecord],
    n: int,
) -> list[tuple[str, ...]]:
    """Generate structural route candidates from explicit Protocol artifact Evidence.

    Evidence must explicitly identify a Protocol artifact path in
    ``transition_data["protocol_path"]``. No path is inferred from prose,
    protocol identifiers, or arbitrary Evidence fields.
    """
    paths: list[Path] = []
    seen: set[str] = set()
    for record in evidence:
        if not isinstance(record, EvidenceRecord):
            raise TypeError("evidence must contain EvidenceRecord instances")
        raw_path = record.transition_data.get("protocol_path")
        if raw_path is None:
            continue
        if not isinstance(raw_path, str) or not raw_path.strip():
            raise ValueError("protocol_path must be a non-empty string")
        if raw_path not in seen:
            seen.add(raw_path)
            paths.append(Path(raw_path))
    return generate_candidates(paths, n)


def render_markdown(candidates: list[tuple[str, ...]], n: int) -> str:
    lines = [
        f"# Protocol Route Candidates (n={n})",
        "",
        "Structural candidates only. Semantic compatibility and execution remain unverified.",
        "",
        "| # | Route |",
        "|---:|---|",
    ]
    for index, route in enumerate(candidates, start=1):
        lines.append(f"| {index} | " + " → ".join(f"`{item}`" for item in route) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--n", type=int, required=True)
    args = parser.parse_args()

    root = Path(args.root)
    paths = sorted((root / "protocols").rglob("*.yaml"))
    print(render_markdown(generate_candidates(paths, args.n), args.n), end="")


if __name__ == "__main__":
    main()
