"""Verify the minimal Background Protocol lifecycle boundary."""

from runtime.background_runner import BackgroundRunner
from runtime.prototype import ExecutionContext, Transition


def anmon_test_protocol(context: ExecutionContext) -> Transition:
    return Transition(
        kind="background.observe",
        data={
            "observed": True,
            "text": context.input.get("text", ""),
            "changed": True,
        },
    )


def main() -> None:
    runner = BackgroundRunner()
    runner.register("anmon_layer_reverse", anmon_test_protocol)

    first = runner.tick({"text": "観測対象"})
    second = runner.tick({"text": "次の観測"})

    assert runner.registered_protocol_ids() == ("anmon_layer_reverse",)
    assert len(first) == 1
    assert len(second) == 1
    assert first[0].result.status == "completed"
    assert second[0].result.status == "completed"
    assert first[0].evidence.protocol_id == "anmon_layer_reverse"
    assert second[0].evidence.protocol_id == "anmon_layer_reverse"
    assert len(runner.landscape.evidence) == 2
    assert runner.landscape.snapshot()["observed"] is True
    print("BACKGROUND_RUNNER VERIFIED")


if __name__ == "__main__":
    main()
