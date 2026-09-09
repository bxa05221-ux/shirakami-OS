"""R0086 Operation automation boundary.

Implementation-only helper for advancing an already validated OperationPlan.
It automates procedural execution steps but does not assign semantic authority,
create new Protocol semantics, or decide whether a result is meaningful.
"""

from dataclasses import dataclass
from typing import Callable, Tuple, Any

from .operation_runner import OperationPlan


@dataclass(frozen=True)
class AutomationStepResult:
    """Observable result of one automation step."""

    step: str
    outcome: str


class OperationAutomationError(ValueError):
    """Raised when an automation request is structurally invalid."""


def automate_operation(
    plan: OperationPlan,
    step_executor: Callable[[str], Any],
) -> Tuple[AutomationStepResult, ...]:
    """Execute the already-defined procedural steps of an OperationPlan.

    The supplied executor owns the external side effect. This boundary only
    follows the deterministic plan and records each step outcome.
    """
    if not isinstance(plan, OperationPlan):
        raise OperationAutomationError("OperationPlan is required")
    if not callable(step_executor):
        raise OperationAutomationError("step_executor is required")

    results = []
    for step in plan.steps:
        outcome = step_executor(step)
        results.append(AutomationStepResult(step=step, outcome=str(outcome)))
    return tuple(results)
