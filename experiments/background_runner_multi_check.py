"""Verify multi-Background Protocol execution remains within its boundary."""

from runtime.background_runner import BackgroundRunner
from runtime.prototype import ExecutionContext, Transition


def first_protocol(context: ExecutionContext) -> Transition:
    return Transition(
        kind="background.observe.first",
        data={"first": True, "changed": True},
    )


def second_protocol(context: ExecutionContext) -> Transition:
    return Transition(
        kind="background.observe.second",
        data={"second": True, "changed": True},
    )


def main() -> None:
    runner = BackgroundRunner()
    runner.register("background.first", first_protocol)
    runner.register("background.second", second_protocol)

    executions = runner.tick({"text": "観測対象"})

    assert runner.registered_protocol_ids() == (
        "background.first",
        "background.second",
    )
    assert len(executions) == 2
    assert tuple(item.protocol_id for item in executions) == (
        "background.first",
        "background.second",
    )
    assert all(item.result.status == "completed" for item in executions)
    assert tuple(item.evidence.protocol_id for item in executions) == (
        "background.first",
        "background.second",
    )
    assert len(runner.landscape.evidence) == 2
    assert runner.landscape.snapshot()["first"] is True
    assert runner.landscape.snapshot()["second"] is True

    # Boundary guard: this runner executes only registered Background Protocols.
    assert "application.protocol" not in runner.registered_protocol_ids()

    print("BACKGROUND_RUNNER_MULTI VERIFIED")


if __name__ == "__main__":
    main()
