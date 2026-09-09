from pathlib import Path

from runtime.landscape import LandscapeState
from runtime.manga_manual import render_manual
from runtime.observable_execution import execute_observably
from runtime.prototype import Runtime, example_protocol


ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "protocols" / "manual" / "manga-user-manual.yaml"


def test_r0071_renderer_projection_does_not_mutate_landscape_or_evidence():
    state = LandscapeState.from_snapshot(
        {"repository": "bxa05221-ux/shirakami-OS", "branch": "main"}
    )
    first = execute_observably(
        state, Runtime(), "example.protocol", example_protocol, {"message": "r0071-first"}
    )
    second = execute_observably(
        state, Runtime(), "example.protocol", example_protocol, {"message": "r0071-second"}
    )

    before_render = state.snapshot()
    evidence_before_render = tuple(state.evidence)
    svg = render_manual(MANUAL, "ja")

    assert "<svg" in svg
    assert "Shirakami OS User Manual Manga" in svg
    assert first.after_state == second.before_state
    assert state.snapshot() == before_render
    assert tuple(state.evidence) == evidence_before_render
    assert len(state.evidence) == 2
    assert [item.protocol_id for item in state.evidence] == [
        "example.protocol",
        "example.protocol",
    ]
