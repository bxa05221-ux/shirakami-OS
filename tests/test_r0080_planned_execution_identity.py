from runtime.execution_request import ExecutionRequest
from runtime.operation_runner import OperationDefinition, plan_operation
from runtime.planned_execution import PlannedExecution


def make_plan(operation_id: str = "R0080"):
    return plan_operation(
        OperationDefinition(
            operation_id=operation_id,
            base_ref="main",
            scope="implementation/operation",
        )
    )


def test_planned_execution_preserves_request_identity():
    request = ExecutionRequest(operation_id="R0080", execution_id="exec-1")
    planned = PlannedExecution(request=request, plan=make_plan())

    assert planned.identity == ("R0080", "exec-1")
    assert planned.request is request


def test_planned_execution_binds_the_validated_plan():
    request = ExecutionRequest(operation_id="R0080", execution_id="exec-1")
    plan = make_plan()
    planned = PlannedExecution(request=request, plan=plan)

    assert planned.plan is plan
    assert planned.plan.operation_id == planned.request.operation_id


def test_planned_execution_rejects_operation_id_mismatch():
    request = ExecutionRequest(operation_id="R0080", execution_id="exec-1")
    plan = make_plan("R0081")

    try:
        PlannedExecution(request=request, plan=plan)
    except ValueError as exc:
        assert str(exc) == "operation_id does not match operation plan"
    else:
        raise AssertionError("operation_id mismatch must be rejected")


def test_planned_execution_has_no_execution_method():
    request = ExecutionRequest(operation_id="R0080", execution_id="exec-1")
    planned = PlannedExecution(request=request, plan=make_plan())

    assert not hasattr(planned, "execute")
