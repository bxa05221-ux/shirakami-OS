import pytest

from runtime.operation_runner import OperationDefinition, plan_operation


def test_r0071_runner_builds_deterministic_operation_plan():
    operation = OperationDefinition(
        operation_id="R0071",
        base_ref="main",
        scope="documentation-only operational observation",
    )

    plan = plan_operation(operation)

    assert plan.operation_id == "R0071"
    assert plan.base_ref == "main"
    assert plan.verification_gate == "test-runtime"
    assert plan.steps == (
        "run-test-runtime",
        "create-artifact",
        "create-protected-pr",
    )


def test_r0071_runner_rejects_forbidden_scope():
    operation = OperationDefinition(
        operation_id="R0071",
        base_ref="main",
        scope="new theory",
    )

    with pytest.raises(ValueError, match="forbidden operation scope"):
        plan_operation(operation)


def test_r0071_runner_rejects_noncanonical_gate():
    operation = OperationDefinition(
        operation_id="R0071",
        base_ref="main",
        scope="documentation-only operational observation",
        verification_gate="other-gate",
    )

    with pytest.raises(ValueError, match="unsupported verification gate"):
        plan_operation(operation)
