"""Detect Protocol composition signals from Shirakami Protocol artifacts.

This is a structural detector, not a semantic compatibility solver.
It identifies explicit input/output/pipeline/flow declarations and reports
candidate predecessor/successor signals for human verification.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def scalar(text: str, key: str) -> str | None:
    m = re.search(rf"^\s*{re.escape(key)}:\s*[\"\']?([^\n\"\']+)", text, re.M)
    return m.group(1).strip() if m else None


def list_values(text: str, section: str) -> list[str]:
    m = re.search(rf"^\s*{re.escape(section)}:\s*\n((?:^[ ]+.*\n?)*)", text, re.M)
    if not m:
        return []
    return [
        x.strip()[2:].strip().strip("\"\'")
        for x in m.group(1).splitlines()
        if x.strip().startswith("- ")
    ]


def route_values(text: str) -> list[str]:
    return re.findall(r"^\s*-\s*(?:phase|name):\s*([^\n]+)", text, re.M)


def detect(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    inputs = list_values(text, "input")
    outputs = list_values(text, "output")
    routes = route_values(text)
    flow = re.search(r"^\s*flow:\s*\n((?:^[ ]+-.*\n?)+)", text, re.M)
    flows = (
        [x.strip()[2:].strip() for x in flow.group(1).splitlines() if x.strip().startswith("- ")]
        if flow
        else []
    )
    return {
        "file": str(path),
        "title": scalar(text, "title") or scalar(text, "name"),
        "version": scalar(text, "version"),
        "inputs": inputs,
        "outputs": outputs,
        "route": routes or flows,
        "signals": {
            "has_input": bool(inputs),
            "has_output": bool(outputs),
            "has_route": bool(routes or flows),
            "has_evidence": "evidence" in text.lower(),
            "has_landscape": "landscape" in text.lower(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root)
    results = [detect(p) for p in sorted((root / "protocols").rglob("*.yaml"))]
    print("# Protocol Composition Detection\n")
    print("Structural detection only. Compatibility is not inferred.\n")
    print("| Artifact | Input | Output | Route | Evidence | Landscape |")
    print("|---|---|---|---|---|---|")
    for item in results:
        s = item["signals"]
        print(
            "| `{}` | {} | {} | {} | {} | {} |".format(
                item["file"],
                "yes" if s["has_input"] else "-",
                "yes" if s["has_output"] else "-",
                ", ".join(item["route"]) if item["route"] else "-",
                "yes" if s["has_evidence"] else "-",
                "yes" if s["has_landscape"] else "-",
            )
        )


if __name__ == "__main__":
    main()
