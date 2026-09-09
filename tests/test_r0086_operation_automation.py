import pytest

from runtime.operation_automation import (
    AutomationStepResult,
    OperationAutomationError,
    automate_operation,
)
from runtime.operation_runner import OperationDefinition, plan_operation


def test_r0086_automates_only_planned_steps():
    plan = plan_operation(
        OperationDefinition(
            operation_id="r0086",
            base_ref="main",
            scope="operation automation boundary",
        )
    )
    seen = []

    def executor(step):
        seen.append(step)
        return "ok"

    result = automate_operation(plan, executor)

    assert seen == list(plan.steps)
    assert result == tuple(
        AutomationStepResult(step=step, outcome="ok") for step in plan.steps
    )


def test_r0086_rejects_invalid_plan():
    with pytest.raises(OperationAutomationError):
        automate_operation(None, lambda step: "ok")


def test_r0086_rejects_missing_executor():
    plan = plan_operation(
        OperationDefinition(
            operation_id="r0086",
            base_ref="main",
            scope="operation automation boundary",
        )
    )
    with pytest.raises(OperationAutomationError):
        automate_operation(plan, None)
