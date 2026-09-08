import json
from pathlib import Path

from runtime.writer_support import support_writer


FIXTURE = Path(__file__).parent / "fixtures" / "dogfight_scene.json"


def test_dogfight_real_landscape_keeps_viewpoints_and_questions_separate():
    landscape = json.loads(FIXTURE.read_text(encoding="utf-8"))
    result = support_writer(landscape)

    assert result.landscape["title"] == "ドッグファイト"
    assert len(result.viewpoints) == len(landscape["observations"])
    assert [view.text for view in result.viewpoints] == landscape["observations"]
    assert result.unresolved_question is None
    assert result.unresolved_questions == tuple(landscape["unresolved_questions"])

    # Re-expression may connect viewpoints, but must not turn the authored
    # unresolved questions into asserted facts.
    for question in landscape["unresolved_questions"]:
        assert question not in result.reexpression
