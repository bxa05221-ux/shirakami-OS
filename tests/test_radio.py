from runtime.radio import render_radio


def test_radio_renders_landscape_through_existing_viewpoint_path():
    landscape = {
        "title": "今日の景色",
        "observations": [
            "朝から雨が降っている。",
            "それでも町には人が歩いている。",
        ],
        "unresolved_questions": ["この雨は今日の予定をどう変えるだろうか。"],
    }

    result = render_radio(landscape)

    assert result.landscape["title"] == "今日の景色"
    assert [view.text for view in result.viewpoints] == landscape["observations"]
    assert result.script.startswith("Shirakami Radio、今日の景色です。")
    assert result.unresolved_questions == tuple(landscape["unresolved_questions"])
    assert landscape["unresolved_questions"][0] not in result.script


def test_radio_asks_when_observable_scene_is_missing():
    result = render_radio({"title": "空のLandscape"})

    assert result.viewpoints == ()
    assert result.unresolved_questions == ()
    assert "教えてください" in result.script
