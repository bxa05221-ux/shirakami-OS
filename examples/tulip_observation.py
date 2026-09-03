"""Tulip example: explicit observations become Landscape evidence.

The example keeps observation, interpretation, and destination separate.
"""

from shirakami_os import ShirakamiOS
from runtime.prototype import ExecutionContext, Transition


def observed_step(context: ExecutionContext) -> Transition:
    return Transition(
        kind="landscape.observation.step",
        data={
            "changed": True,
            "stage": context.input["stage"],
            "observed": context.input["observed"],
            "relation": context.input.get("relation"),
        },
    )


def main() -> None:
    os = ShirakamiOS()
    os.boot({"stage": "チューリップ"})

    observations = [
        {
            "stage": "最初の演奏",
            "observed": {"sound": "まだ不揃い"},
        },
        {
            "stage": "なんとかなった",
            "observed": {"sound": "最後まで演奏できた"},
        },
        {
            "stage": "誰かが聴いてくれた",
            "observed": {"listener": "聴いてくれる人がいた"},
        },
        {
            "stage": "毎日楽しみに聞いてくれる人がいる",
            "observed": {"listener": "毎日楽しみに聞いてる"},
        },
    ]

    for item in observations:
        result = os.execute(
            "example.landscape.observation",
            observed_step,
            item,
        )
        print(f"current: {result.landscape['stage']}")
        print(f"observed: {dict(result.landscape['observed'])}")
        if result.landscape.get("relation"):
            print(f"relation: {result.landscape['relation']}")
        print(f"evidence_count: {len(os.landscape.evidence)}")
        print()

    print("navigation:", dict(os.navigation.snapshot()))


if __name__ == "__main__":
    main()
