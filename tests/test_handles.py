import pytest

from runtime.choice import HandleChoice, choose_handle
from runtime.handles import HandleSet, offer_handles, select_handle
from runtime.observation import ObservationRequest
from shirakami_os import ShirakamiOS


def test_multiple_handles_are_offered_without_mutating_landscape():
    os = ShirakamiOS()
    os.boot({"stage": "吹雪の中を新聞配達"})

    views = [
        os.reobserve(
            ObservationRequest(
                concern="今日はきつい",
                lens="weather",
                parameters={"observed": {"weather": "吹雪"}},
            )
        ),
        os.reobserve(
            ObservationRequest(
                concern="今日はきつい",
                lens="companion",
                parameters={"observed": {"companion": "オレ炬燵の中"}},
            )
        ),
        os.reobserve(
            ObservationRequest(
                concern="今日はきつい",
                lens="route",
                parameters={"observed": {"route": "あと三軒"}},
            )
        ),
    ]

    offered = offer_handles(
        views,
        labels={
            "weather": "天気から見てみる",
            "companion": "名無しと話してみる",
            "route": "あとどれくらいか見てみる",
        },
    )

    assert isinstance(offered, HandleSet)
    assert [handle.lens for handle in offered.handles] == [
        "weather",
        "companion",
        "route",
    ]
    assert offered.handles[1].observed == {"companion": "オレ炬燵の中"}
    assert os.landscape.snapshot()["stage"] == "吹雪の中を新聞配達"
    assert len(os.landscape.evidence) == 0


def test_human_selects_one_handle_explicitly():
    os = ShirakamiOS()
    os.boot({"stage": "吹雪の中を新聞配達"})

    views = [
        os.reobserve(
            ObservationRequest(
                concern="寒い",
                lens="weather",
                parameters={"observed": {"weather": "吹雪"}},
            )
        ),
        os.reobserve(
            ObservationRequest(
                concern="寒い",
                lens="companion",
                parameters={"observed": {"companion": "オレ炬燵の中"}},
            )
        ),
    ]
    offered = offer_handles(views)

    selected = select_handle(offered, "handle:companion")
    choice = choose_handle(selected)

    assert isinstance(choice, HandleChoice)
    assert choice.handle_id == "handle:companion"
    assert os.landscape.snapshot()["stage"] == "吹雪の中を新聞配達"
    assert len(os.landscape.evidence) == 0


def test_duplicate_lenses_are_rejected():
    view = ObservationRequest(
        concern="確認",
        lens="same",
        parameters={"observed": {}},
    )
    os = ShirakamiOS()
    os.boot({"stage": "current"})
    first = os.reobserve(view)
    second = os.reobserve(view)

    with pytest.raises(ValueError):
        offer_handles([first, second])


def test_select_handle_requires_explicit_existing_id():
    os = ShirakamiOS()
    os.boot({"stage": "current"})
    offered = offer_handles(
        [
            os.reobserve(
                ObservationRequest(
                    concern="確認",
                    lens="listener",
                    parameters={"observed": {}},
                )
            )
        ]
    )

    with pytest.raises(KeyError):
        select_handle(offered, "handle:not-offered")
