from runtime.execution_planner import plan_execution_request
from runtime.execution_request import ExecutionRequest
from runtime.operation_executor import OperationExecutor
from runtime.operation_runner import OperationDefinition
from runtime.planned_execution import PlannedExecution


def make_planned(execution_id: str = "exec-1"):
    operation = OperationDefinition(
        operation_id="R0083",
        base_ref="main",
        scope="implementation/operation",
    )
    request = ExecutionRequest(operation_id="R0083", execution_id=execution_id)
    plan = plan_execution_request(request, operation)
    return PlannedExecution(request=request, plan=plan)


def test_executor_returns_result_with_planned_identity():
    planned = make_planned()
    result = OperationExecutor().execute(planned, "completed")

    assert result.identity == ("R0083", "exec-1")
    assert result.outcome == "completed"


def test_executor_keeps_distinct_execution_identity():
    executor = OperationExecutor()
    first = executor.execute(make_planned("exec-1"), "completed")
    second = executor.execute(make_planned("exec-2"), "completed")

    assert first.identity != second.identity


def test_executor_does_not_change_planned_execution():
    planned = make_planned()
    executor = OperationExecutor()
    executor.execute(planned, "completed")

    assert planned.identity == ("R0083", "exec-1")
