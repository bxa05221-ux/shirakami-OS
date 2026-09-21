"""Five-minute demonstration of the Evidence → Human Gate → Runtime loop.

Run from the repository root:

    python examples/evidence_route_demo.py

The demo uses temporary Protocol YAML artifacts, derives a structural
candidate from explicit Evidence, pauses at HUMAN_REVIEW, then performs an
explicit human approval in code and executes the selected route.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from runtime.evidence import EvidenceRecord
from runtime.one_stroke_route_pipeline import OneStrokeRoutePipeline
from runtime.prototype import ExecutionContext, Transition


def protocol(name: str, suffix: str):
    def run(context: ExecutionContext) -> Transition:
        value = context.input.get("value", "")
        return Transition(
            kind=f"step.{name}",
            data={"value": f"{value}{suffix}"},
        )

    return run


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="shirakami-demo-") as work:
        root = Path(work)
        first = root / "01_append_a.yaml"
        second = root / "02_append_b.yaml"
        first.write_text("title: Append A\noutput:\n  - shared\n", encoding="utf-8")
        second.write_text("title: Append B\ninput:\n  - shared\n", encoding="utf-8")

        evidence = (
            EvidenceRecord(
                protocol_id="observed.a",
                status="observed",
                transition_kind="protocol.observed",
                transition_data={"protocol_path": str(first)},
                signals=("PROTOCOL_ARTIFACT",),
            ),
            EvidenceRecord(
                protocol_id="observed.b",
                status="observed",
                transition_kind="protocol.observed",
                transition_data={"protocol_path": str(second)},
                signals=("PROTOCOL_ARTIFACT",),
            ),
        )

        pipeline = OneStrokeRoutePipeline()

        print("1. Evidence → structural Candidate")
        candidates = pipeline.propose_candidates_from_evidence(evidence, n=2)
        if not candidates:
            raise RuntimeError("demo produced no structural candidate")
        candidate = candidates[0]
        print(f"   candidate: {candidate}")

        print("2. Candidate → HUMAN_REVIEW")
        pipeline.prepare_candidate("demo", candidate, reviewer="human")
        print(f"   state: {pipeline.runtime.loop.state.value}")

        print("3. Human Gate → READY")
        # Deliberate authorization point: proposal alone cannot execute.
        pipeline.approve_candidate(approved=True)
        print(f"   state: {pipeline.runtime.loop.state.value}")

        print("4. One-Stroke Runtime → Verification")
        result = pipeline.execute(
            {
                str(first): protocol("a", "A"),
                str(second): protocol("b", "B"),
            },
            {"value": ""},
        )
        print(f"   route: {result.execution.transition.data['route']}")
        print(f"   result: {result.execution.transition.data['final']['value']}")
        print(f"   verification: {result.verification.status}")
        print(f"   state: {pipeline.runtime.loop.state.value}")

        print("5. Evidence retained")
        print(f"   evidence records: {len(result.evidence)}")
        print("   cycle complete: Evidence → Candidate → Human Gate → Runtime → Evidence")


if __name__ == "__main__":
    main()
