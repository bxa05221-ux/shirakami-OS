import pytest

from runtime.choice import HandleChoice, choose_handle
from runtime.handle import offer_handle
from runtime.observation import ObservationRequest
from shirakami_os import ShirakamiOS


def test_human_choice_records_selected_handle_without_landscape_change():
    os = ShirakamiOS()
    os.boot({"stage": "なんとかなった"})

    view = os.reobserve(
        ObservationRequest(
            concern="上手くなっていない気がする",
            lens="listener",
            parameters={"observed": {"listener": "毎日楽しみに聞いてる"}},
        )
    )
    handle = offer_handle(view, label="聴いてくれている人から見てみる")

    choice = choose_handle(handle)

    assert isinstance(choice, HandleChoice)
    assert choice.handle_id == handle.id
    assert choice.actor == "human"
    assert os.landscape.snapshot()["stage"] == "なんとかなった"
    assert len(os.landscape.evidence) == 0


def test_choice_rejects_non_handle_and_empty_actor():
    with pytest.raises(TypeError):
        choose_handle("not-a-handle")  # type: ignore[arg-type]

    os = ShirakamiOS()
    os.boot({"stage": "なんとかなった"})
    view = os.reobserve(
        ObservationRequest(
            concern="確認",
            lens="listener",
            parameters={"observed": {}},
        )
    )
    handle = offer_handle(view)

    with pytest.raises(ValueError):
        choose_handle(handle, actor=" ")
