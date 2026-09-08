import pytest

from runtime.choice import choose_handle
from runtime.handle import offer_handle
from runtime.outcome import (
    HandleOutcome,
    observe_handle_outcome,
    outcome_transition,
)
from runtime.observation import ObservationRequest
from runtime.prototype import ExecutionContext
from shirakami_os import ShirakamiOS


def test_choice_then_observed_outcome_changes_landscape_through_runtime():
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

    assert os.landscape.snapshot()["stage"] == "なんとかなった"
    assert len(os.landscape.evidence) == 0

    outcome = observe_handle_outcome(
        choice,
        {"stage": "町に聞いてもらった", "listener": "毎日楽しみに聞いてる"},
    )
    assert isinstance(outcome, HandleOutcome)
    assert os.landscape.snapshot()["stage"] == "なんとかなった"

    def apply_outcome(context: ExecutionContext):
        return outcome_transition(outcome)

    result = os.execute("handle.outcome", apply_outcome)

    assert result.transition.kind == "landscape.handle.outcome"
    assert result.evidence.transition_data["stage"] == "町に聞いてもらった"
    assert os.landscape.snapshot()["stage"] == "町に聞いてもらった"
    assert os.landscape.snapshot()["listener"] == "毎日楽しみに聞いてる"
    assert len(os.landscape.evidence) == 1


def test_outcome_does_not_infer_or_declare_success():
    os = ShirakamiOS()
    os.boot({"stage": "なんとかなった"})
    view = os.reobserve(
        ObservationRequest(
            concern="確認",
            lens="listener",
            parameters={"observed": {}},
        )
    )
    choice = choose_handle(offer_handle(view))
    outcome = observe_handle_outcome(choice, {"stage": "町に聞いてもらった"})
    transition = outcome_transition(outcome)

    assert transition.data["changed"] is True
    assert "success" not in transition.data
    assert "decision" not in transition.data


def test_outcome_rejects_unobserved_or_invalid_inputs():
    with pytest.raises(TypeError):
        observe_handle_outcome("not-a-choice", {})  # type: ignore[arg-type]

    os = ShirakamiOS()
    os.boot()
    view = os.reobserve(
        ObservationRequest(concern="確認", lens="listener", parameters={"observed": {}})
    )
    choice = choose_handle(offer_handle(view))

    with pytest.raises(TypeError):
        observe_handle_outcome(choice, "not-a-mapping")  # type: ignore[arg-type]
