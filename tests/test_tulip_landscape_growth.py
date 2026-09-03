from shirakami_os import ShirakamiOS
from runtime.prototype import ExecutionContext, Transition


def growth_step(context: ExecutionContext) -> Transition:
    """A deliberately small protocol for advancing one observed story step."""
    return Transition(
        kind="landscape.growth.step",
        data={
            "changed": True,
            "stage": context.input["stage"],
            "from_stage": context.input.get("from_stage"),
        },
    )


def test_tulip_becomes_the_next_current_position():
    os = ShirakamiOS()
    os.boot({"stage": "チューリップ"})

    steps = [
        "最初の演奏",
        "なんとかなった",
        "誰かが聴いてくれた",
        "毎日楽しみに聞いてくれる人がいる",
        "仲間が増えた",
        "もっと上手くなりたい",
    ]

    previous = "チューリップ"
    for stage in steps:
        result = os.execute(
            "example.landscape.growth",
            growth_step,
            {"from_stage": previous, "stage": stage},
        )

        assert result.status == "completed"
        assert result.evidence.transition_data["changed"] is True
        assert result.evidence.transition_data["from_stage"] == previous
        assert result.landscape["stage"] == stage

        # The newly observed state is now the next current position.
        previous = stage

    assert os.landscape.evidence[-1].transition_data["stage"] == "もっと上手くなりたい"
    assert len(os.landscape.evidence) == len(steps)


def test_tulip_growth_does_not_require_a_destination():
    os = ShirakamiOS()
    os.boot({"stage": "チューリップ"})

    result = os.execute(
        "example.landscape.growth",
        growth_step,
        {"from_stage": "チューリップ", "stage": "最初の演奏"},
    )

    assert result.landscape["stage"] == "最初の演奏"
    assert "destination" not in result.landscape
    assert "destination" not in result.navigation
