from shirakami_os import ShirakamiOS
from runtime.prototype import ExecutionContext, Transition


def observed_step(context: ExecutionContext) -> Transition:
    """Pass through explicitly observed fields without interpreting them."""
    return Transition(
        kind="landscape.observation.step",
        data={
            "changed": True,
            "stage": context.input["stage"],
            "observed": context.input["observed"],
            "relation": context.input.get("relation"),
        },
    )


def test_tulip_landscape_keeps_observation_separate_from_interpretation():
    os = ShirakamiOS()
    os.boot({"stage": "チューリップ", "observed": {"sound": "まだ不揃い"}})

    result = os.execute(
        "example.landscape.observation",
        observed_step,
        {
            "stage": "なんとかなった",
            "observed": {"sound": "最後まで演奏できた"},
            "relation": "誰かが聴いてくれた",
        },
    )

    assert result.status == "completed"
    assert result.landscape["stage"] == "なんとかなった"
    assert result.landscape["observed"] == {"sound": "最後まで演奏できた"}
    assert result.landscape["relation"] == "誰かが聴いてくれた"

    # The Runtime stores what was explicitly observed; it does not add a diagnosis,
    # value judgment, or destination.
    assert "diagnosis" not in result.landscape
    assert "judgment" not in result.landscape
    assert "destination" not in result.landscape


def test_tulip_listener_is_evidence_not_a_success_score():
    os = ShirakamiOS()
    os.boot({"stage": "誰かが聴いてくれた"})

    result = os.execute(
        "example.landscape.observation",
        observed_step,
        {
            "stage": "毎日楽しみに聞いてくれる人がいる",
            "observed": {"listener": "毎日楽しみに聞いてる"},
        },
    )

    evidence = result.evidence.transition_data
    assert evidence["observed"]["listener"] == "毎日楽しみに聞いてる"
    assert "score" not in evidence
    assert "success" not in evidence
