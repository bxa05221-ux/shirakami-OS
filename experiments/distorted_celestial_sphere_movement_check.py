"""Verify minimal temporal tracking of one observed star.

Implementation-boundary experiment only: it preserves observations across turns
without inferring meaning or forming a constellation.
"""

from runtime.background_runner import BackgroundRunner
from runtime.prototype import ExecutionContext, Transition


def observe_star(context: ExecutionContext) -> Transition:
    text = context.input.get("text", "")
    star_id = context.input.get("star_id", "star-001")
    return Transition(
        kind="cognitive_space.star.observed",
        data={
            "star": {
                "id": star_id,
                "content": text,
                "distance": context.input.get("distance"),
                "brightness": context.input.get("brightness"),
                "phase": context.input.get("phase"),
            },
            "constellation": None,
            "semantic_interpretation": False,
            "changed": True,
        },
    )


def main() -> None:
    runner = BackgroundRunner()
    runner.register("distorted-celestial-sphere-protocol", observe_star)

    first = runner.tick({
        "star_id": "star-001",
        "text": "星が見えにくい",
        "distance": None,
        "brightness": 0.4,
        "phase": "quiet",
    })[0]
    second = runner.tick({
        "star_id": "star-001",
        "text": "さっきの星が少し見えてきた",
        "distance": None,
        "brightness": 0.7,
        "phase": "emerging",
    })[0]

    first_star = first.result.transition.data["star"]
    second_star = second.result.transition.data["star"]

    assert first_star["id"] == second_star["id"] == "star-001"
    assert first_star["content"] == "星が見えにくい"
    assert second_star["content"] == "さっきの星が少し見えてきた"
    assert first_star["brightness"] == 0.4
    assert second_star["brightness"] == 0.7
    assert first_star["phase"] == "quiet"
    assert second_star["phase"] == "emerging"
    assert first.result.transition.data["constellation"] is None
    assert second.result.transition.data["constellation"] is None
    assert first.result.transition.data["semantic_interpretation"] is False
    assert second.result.transition.data["semantic_interpretation"] is False
    assert len(runner.landscape.evidence) == 2

    print("DISTORTED_CELESTIAL_SPHERE_STAR MOVEMENT VERIFIED")


if __name__ == "__main__":
    main()
