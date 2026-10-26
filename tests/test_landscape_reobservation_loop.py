from runtime.choice import choose_handle
from runtime.handle import offer_handle
from runtime.observation import ObservationRequest
from runtime.outcome import observe_handle_outcome, outcome_transition
from runtime.prototype import ExecutionContext
from shirakami_os import ShirakamiOS


def test_landscape_evidence_becomes_next_observation_point():
    os = ShirakamiOS()
    os.boot({"stage": "なんとかなった"})

    first_view = os.reobserve(
        ObservationRequest(
            concern="上手くなっていない気がする",
            lens="listener",
            parameters={"observed": {"listener": "まだ誰も聴いていない"}},
        )
    )
    choice = choose_handle(
        offer_handle(first_view, label="聴いてくれている人から見てみる")
    )
    outcome = observe_handle_outcome(
        choice,
        {"stage": "町に聞いてもらった", "listener": "毎日楽しみに聞いてる"},
    )

    def apply_outcome(context: ExecutionContext):
        return outcome_transition(outcome)

    os.execute("handle.outcome", apply_outcome)

    second_view = os.reobserve(
        ObservationRequest(
            concern="次はどう見えるだろう",
            lens="listener",
            parameters={"observed": os.landscape.snapshot()},
        )
    )

    assert second_view.source_revision is None
    assert second_view.observed["stage"] == "町に聞いてもらった"
    assert second_view.observed["listener"] == "毎日楽しみに聞いてる"
    assert len(os.landscape.evidence) == 1
