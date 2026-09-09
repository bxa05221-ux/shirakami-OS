from runtime.execution_boundary import ExecutionBoundary
from runtime.execution_request import ExecutionRequest
from runtime.operation_result import OperationResult
from runtime.operation_runner import OperationDefinition, plan_operation
from runtime.planned_execution import PlannedExecution


def make_planned(operation_id: str = "R0081", execution_id: str = "exec-1"):
    request = ExecutionRequest(operation_id=operation_id, execution_id=execution_id)
    plan = plan_operation(
        OperationDefinition(
            operation_id=operation_id,
            base_ref="main",
            scope="implementation/operation",
        )
    )
    return PlannedExecution(request=request, plan=plan)


def test_execution_boundary_preserves_execution_identity():
    planned = make_planned()
    result = OperationResult(operation_id="R0081", execution_id="exec-1", outcome="observed")

    boundary = ExecutionBoundary(planned=planned, result=result)

    assert boundary.identity == ("R0081", "exec-1")
    assert boundary.planned is planned
    assert boundary.result is result


def test_execution_boundary_rejects_identity_mismatch():
    planned = make_planned()
    result = OperationResult(operation_id="R0081", execution_id="exec-2", outcome="observed")

    try:
        ExecutionBoundary(planned=planned, result=result)
    except ValueError as exc:
        assert str(exc) == "operation execution identity does not match planned execution"
    else:
        raise AssertionError("execution identity mismatch must be rejected")


def test_execution_boundary_has_no_execute_method():
    boundary = ExecutionBoundary(
        planned=make_planned(),
        result=OperationResult(operation_id="R0081", execution_id="exec-1", outcome="observed"),
    )

    assert not hasattr(boundary, "execute")
