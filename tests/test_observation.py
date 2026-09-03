from runtime.observation import ObservationRequest, reobserve


def test_reobserve_changes_the_view_not_the_landscape():
    landscape = {
        "stage": "なんとかなった",
        "observed": {"sound": "最後まで演奏できた"},
        "relation": "誰かが聴いてくれた",
    }
    before = dict(landscape)

    view = reobserve(
        landscape,
        ObservationRequest(
            concern="上手くなっていない気がする",
            lens="listener",
            parameters={
                "observed": {"listener": "毎日楽しみに聞いてる"},
                "uncertainty": ("演奏技術が実際に向上したかは未観測",),
            },
        ),
    )

    assert landscape == before
    assert view.concern == "上手くなっていない気がする"
    assert view.lens == "listener"
    assert view.observed == {"listener": "毎日楽しみに聞いてる"}
    assert view.uncertainty == ("演奏技術が実際に向上したかは未観測",)


def test_reobservation_does_not_turn_interpretation_into_fact():
    landscape = {"stage": "なんとかなった"}

    view = reobserve(
        landscape,
        ObservationRequest(
            concern="この活動には意味があるのか",
            lens="relation",
            parameters={
                "observed": {"listener": "毎日楽しみに聞いてる"},
            },
        ),
    )

    assert "diagnosis" not in view.observed
    assert "judgment" not in view.observed
    assert "score" not in view.observed
    assert "success" not in view.observed
    assert "destination" not in view.observed
