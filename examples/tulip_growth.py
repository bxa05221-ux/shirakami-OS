"""Executable Tulip landscape-growth example.

The example deliberately keeps the protocol small: each observed step becomes
an Evidence-backed current position for the next step. No destination is set.
"""

from shirakami_os import ShirakamiOS
from runtime.prototype import ExecutionContext, Transition


def growth_step(context: ExecutionContext) -> Transition:
    return Transition(
        kind="landscape.growth.step",
        data={
            "changed": True,
            "stage": context.input["stage"],
            "from_stage": context.input.get("from_stage"),
        },
    )


def main() -> None:
    os = ShirakamiOS()
    os.boot({"stage": "チューリップ"})

    stages = [
        "最初の演奏",
        "なんとかなった",
        "誰かが聴いてくれた",
        "毎日楽しみに聞いてくれる人がいる",
        "仲間が増えた",
        "もっと上手くなりたい",
    ]

    previous = "チューリップ"
    for stage in stages:
        result = os.execute(
            "example.landscape.growth",
            growth_step,
            {"from_stage": previous, "stage": stage},
        )
        print(f"{previous} -> {stage}")
        print(f"  evidence: {dict(result.evidence.transition_data)}")
        print(f"  current: {result.landscape['stage']}")
        previous = stage

    print("destination:", os.navigation.snapshot()["horizon"])


if __name__ == "__main__":
    main()
