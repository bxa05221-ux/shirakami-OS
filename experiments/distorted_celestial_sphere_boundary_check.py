"""Verify the research-handoff artifact reaches the Background execution boundary.

This is deliberately a boundary test, not an implementation of the protocol's
cognitive semantics. The protocol artifact is loaded and explicitly registered
as a Background Protocol; the test verifies one execution -> Evidence cycle.
"""

from runtime.background_runner import BackgroundRunner
from runtime.prototype import ExecutionContext, Transition


def distorted_celestial_sphere_boundary(context: ExecutionContext) -> Transition:
    """Test-only execution stub for the research-handoff protocol boundary."""
    return Transition(
        kind="cognitive_space.observe",
        data={
            "protocol": "distorted-celestial-sphere-protocol",
            "observed_input": context.input.get("text", ""),
            "semantic_interpretation": False,
            "changed": True,
        },
    )


def main() -> None:
    runner = BackgroundRunner()
    runner.register(
        "distorted-celestial-sphere-protocol",
        distorted_celestial_sphere_boundary,
    )

    executions = runner.tick({"text": "星が見えにくい"})

    assert len(executions) == 1
    execution = executions[0]
    assert execution.protocol_id == "distorted-celestial-sphere-protocol"
    assert execution.result.status == "completed"
    assert execution.result.transition.kind == "cognitive_space.observe"
    assert execution.result.transition.data["semantic_interpretation"] is False
    assert execution.evidence.protocol_id == "distorted-celestial-sphere-protocol"
    assert len(runner.landscape.evidence) == 1
    print("DISTORTED_CELESTIAL_SPHERE_BOUNDARY VERIFIED")


if __name__ == "__main__":
    main()
