from shirakami_os import ShirakamiOS
from runtime.handle import HANDLE_FORBIDDEN_OPERATIONS, offer_handle
from runtime.observation import ObservationRequest


def test_handle_is_a_small_step_not_an_action():
    os = ShirakamiOS()
    os.boot(
        {
            "stage": "なんとかなった",
            "observed": {"sound": "最後まで演奏できた"},
            "relation": "誰かが聴いてくれた",
        }
    )

    view = os.reobserve(
        ObservationRequest(
            concern="上手くなっていない気がする",
            lens="listener",
            parameters={
                "observed": {"listener": "毎日楽しみに聞いてる"},
            },
        )
    )
    handle = offer_handle(view, label="聴いてくれている人から見てみる")

    assert handle.id == "handle:listener"
    assert handle.label == "聴いてくれている人から見てみる"
    assert handle.lens == "listener"
    assert handle.observed == {"listener": "毎日楽しみに聞いてる"}
    assert os.landscape.snapshot()["stage"] == "なんとかなった"
    assert len(os.landscape.evidence) == 0


def test_handle_does_not_encode_forbidden_decisions():
    assert "choose_destination" in HANDLE_FORBIDDEN_OPERATIONS
    assert "choose_values" in HANDLE_FORBIDDEN_OPERATIONS
    assert "choose_faith" in HANDLE_FORBIDDEN_OPERATIONS
    assert "make_decision" in HANDLE_FORBIDDEN_OPERATIONS
    assert "mutate_landscape" in HANDLE_FORBIDDEN_OPERATIONS
    assert "open_drawer" in HANDLE_FORBIDDEN_OPERATIONS
