"""Executable smoke test for the paired OPPAI benchmark harness."""

from oppai_benchmark import run_trial, summarize


def mock_adapter(user_input, context):
    return {"accepted": bool(user_input.strip()), "context": dict(context)}


def main():
    trials = [
        run_trial(
            condition="direct",
            task_id="natural-correction-001",
            adapter=mock_adapter,
            user_input="いや、そうじゃない。さっきの案に戻して。",
            context={"topic": "design"},
            elapsed_seconds=30,
            corrections=2,
            re_explanations=1,
            context_recoveries=1,
            completed=True,
            voluntary_continue=True,
            comfort="", friction="",
        ),
        run_trial(
            condition="oppai",
            task_id="natural-correction-001",
            adapter=mock_adapter,
            user_input="いや、そうじゃない。さっきの案に戻して。",
            context={"topic": "design"},
            elapsed_seconds=20,
            corrections=1,
            re_explanations=0,
            context_recoveries=0,
            completed=True,
            voluntary_continue=True,
            comfort="", friction="",
        ),
    ]
    print(summarize(trials))


if __name__ == "__main__":
    main()
