from runtime.writer_support import support_writer


def test_writer_support_exposes_observed_scene_without_taking_over_authorship():
    result = support_writer(
        {
            "scene_id": "scene-001",
            "observations": [
                "主人公は玄関で靴を履いたまま立っている。",
                "雨の音が続いている。",
            ],
        }
    )

    assert result.landscape["scene_id"] == "scene-001"
    assert [view.text for view in result.viewpoints] == [
        "主人公は玄関で靴を履いたまま立っている。",
        "雨の音が続いている。",
    ]
    assert result.unresolved_question is None
    assert "主人公は玄関で靴を履いたまま立っている。" in result.reexpression
    assert "雨の音が続いている。" in result.reexpression


def test_writer_support_asks_when_observable_scene_is_missing():
    result = support_writer({"scene_id": "scene-002"})

    assert result.viewpoints == ()
    assert result.reexpression == ""
    assert result.unresolved_question == "この場面について、まず何が観測されているか教えてください。"


def test_writer_support_does_not_invent_empty_observations():
    result = support_writer({"observations": ["", 42, None]})

    assert result.viewpoints == ()
    assert result.reexpression == ""
