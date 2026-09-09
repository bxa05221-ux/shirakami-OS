from runtime.execution_planner import plan_execution_request
from runtime.execution_request import ExecutionRequest
from runtime.operation_loop_bridge import bridge_operation_result
from runtime.operation_runner import OperationDefinition
from runtime.planned_execution import PlannedExecution


def make_planned(execution_id: str = "exec-1"):
    operation = OperationDefinition(
        operation_id="R0082",
        base_ref="main",
        scope="implementation/operation",
    )
    request = ExecutionRequest(operation_id="R0082", execution_id=execution_id)
    plan = plan_execution_request(request, operation)
    return PlannedExecution(request=request, plan=plan)


def test_operation_loop_bridge_preserves_planned_identity():
    planned = make_planned()
    boundary = bridge_operation_result(planned, "observed")

    assert boundary.identity == ("R0082", "exec-1")
    assert boundary.result.outcome == "observed"


def test_operation_loop_bridge_produces_distinct_result_for_distinct_execution():
    first = make_planned("exec-1")
    second = make_planned("exec-2")

    first_boundary = bridge_operation_result(first, "observed")
    second_boundary = bridge_operation_result(second, "observed")

    assert first_boundary.identity != second_boundary.identity
    assert first_boundary.result is not second_boundary.result


def test_operation_loop_bridge_does_not_execute():
    planned = make_planned()
    bridge = bridge_operation_result(planned, "observed")

    assert not hasattr(bridge, "execute")
