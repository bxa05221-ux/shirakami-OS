from runtime.operation_runner import OperationDefinition, plan_operation


def test_r0072_operation_dispatcher_produces_deterministic_plan():
    operation = OperationDefinition(
        operation_id="R0072",
        base_ref="main",
        scope="documentation-only operational automation",
    )

    plan = plan_operation(operation)

    assert plan.operation_id == "R0072"
    assert plan.base_ref == "main"
    assert plan.verification_gate == "test-runtime"
    assert plan.steps == (
        "record-baseline",
        "create-artifact",
        "run-test-runtime",
        "create-protected-pr",
        "record-merge-result",
    )


def test_r0072_operation_dispatcher_rejects_forbidden_scope():
    operation = OperationDefinition(
        operation_id="R0072",
        base_ref="main",
        scope="new theory",
    )

    try:
        plan_operation(operation)
    except ValueError as exc:
        assert str(exc) == "forbidden operation scope: new theory"
    else:
        raise AssertionError("forbidden scope must be rejected")
