import pytest

from runtime.cycle import CycleStep, begin_cycle, record_cycle_outcome
from runtime.observation import ObservationRequest
from shirakami_os import ShirakamiOS


def test_cycle_reobserves_updated_landscape_and_human_can_choose_again():
    os = ShirakamiOS()
    os.boot({"stage": "なんとかなった"})

    first = begin_cycle(
        os.landscape.snapshot(),
        ObservationRequest(
            concern="上手くなっていない気がする",
            lens="listener",
            parameters={"observed": {"listener": "毎日楽しみに聞いてる"}},
        ),
        label="聴いてくれている人から見てみる",
    )
    assert first.choice.actor == "human"

    outcome = record_cycle_outcome(
        first,
        {"stage": "町に聞いてもらった", "listener": "毎日楽しみに聞いてる"},
    )

    def apply_outcome(_context):
        from runtime.outcome import outcome_transition

        return outcome_transition(outcome)

    result = os.execute("handle.outcome", apply_outcome)
    assert result.landscape["stage"] == "町に聞いてもらった"

    second = begin_cycle(
        os.landscape.snapshot(),
        ObservationRequest(
            concern="今はどう見える？",
            lens="next_step",
            parameters={
                "observed": {
                    "stage": "町に聞いてもらった",
                    "next": "もう一度演奏してみる",
                }
            },
        ),
        label="今の現在地から見てみる",
    )

    assert isinstance(second, CycleStep)
    assert second.view.source_revision is None
    assert second.view.observed["stage"] == "町に聞いてもらった"
    assert second.choice.actor == "human"
    assert os.landscape.snapshot()["stage"] == "町に聞いてもらった"
    assert len(os.landscape.evidence) == 1


def test_cycle_requires_explicit_observed_outcome():
    os = ShirakamiOS()
    os.boot({"stage": "なんとかなった"})
    step = begin_cycle(
        os.landscape.snapshot(),
        ObservationRequest(
            concern="確認",
            lens="listener",
            parameters={"observed": {}},
        ),
    )

    with pytest.raises(TypeError):
        record_cycle_outcome(step, "not-a-mapping")  # type: ignore[arg-type]
