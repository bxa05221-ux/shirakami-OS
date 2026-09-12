"""Verify the minimal observable star representation for the research handoff.

This remains an implementation-boundary experiment. It does not infer meaning,
form constellations, or implement the full research semantics.
"""

from runtime.background_runner import BackgroundRunner
from runtime.prototype import ExecutionContext, Transition


def observe_star(context: ExecutionContext) -> Transition:
    text = context.input.get("text", "")
    return Transition(
        kind="cognitive_space.star.observed",
        data={
            "star": {
                "content": text,
                "distance": None,
                "brightness": None,
                "phase": None,
            },
            "constellation": None,
            "semantic_interpretation": False,
            "changed": True,
        },
    )


def main() -> None:
    runner = BackgroundRunner()
    runner.register("distorted-celestial-sphere-protocol", observe_star)

    executions = runner.tick({"text": "星が見えにくい"})
    assert len(executions) == 1

    execution = executions[0]
    star = execution.result.transition.data["star"]
    assert star["content"] == "星が見えにくい"
    assert star["distance"] is None
    assert star["brightness"] is None
    assert star["phase"] is None
    assert execution.result.transition.data["constellation"] is None
    assert execution.result.transition.data["semantic_interpretation"] is False
    assert execution.evidence.protocol_id == "distorted-celestial-sphere-protocol"
    assert len(runner.landscape.evidence) == 1
    print("DISTORTED_CELESTIAL_SPHERE_STAR OBSERVATION VERIFIED")


if __name__ == "__main__":
    main()
