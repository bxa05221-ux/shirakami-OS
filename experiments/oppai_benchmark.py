"""Small paired harness for measuring OPPAI operational friction.

This harness deliberately measures the human-facing interaction cost rather
than model benchmark scores. A real adapter can be supplied later.
"""

from dataclasses import dataclass, asdict
from typing import Any, Callable, Mapping


@dataclass
class Trial:
    condition: str
    task_id: str
    elapsed_seconds: float
    corrections: int
    re_explanations: int
    context_recoveries: int
    completed: bool
    voluntary_continue: bool
    comfort: str = ""
    friction: str = ""


def run_trial(
    *,
    condition: str,
    task_id: str,
    adapter: Callable[[str, Mapping[str, Any]], Any],
    user_input: str,
    context: Mapping[str, Any] | None = None,
    elapsed_seconds: float = 0.0,
    corrections: int = 0,
    re_explanations: int = 0,
    context_recoveries: int = 0,
    completed: bool = True,
    voluntary_continue: bool = False,
    comfort: str = "",
    friction: str = "",
) -> Trial:
    adapter(user_input, context or {})
    return Trial(condition, task_id, elapsed_seconds, corrections,
                 re_explanations, context_recoveries, completed,
                 voluntary_continue, comfort, friction)


def summarize(trials: list[Trial]) -> dict[str, Any]:
    if not trials:
        return {"count": 0}
    return {
        "count": len(trials),
        "mean_elapsed_seconds": sum(t.elapsed_seconds for t in trials) / len(trials),
        "mean_corrections": sum(t.corrections for t in trials) / len(trials),
        "mean_re_explanations": sum(t.re_explanations for t in trials) / len(trials),
        "mean_context_recoveries": sum(t.context_recoveries for t in trials) / len(trials),
        "completion_rate": sum(t.completed for t in trials) / len(trials),
        "voluntary_continue_rate": sum(t.voluntary_continue for t in trials) / len(trials),
    }


def export_trial(trial: Trial) -> dict[str, Any]:
    return asdict(trial)
