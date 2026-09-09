from runtime.execution_planner import plan_execution_request
from runtime.execution_request import ExecutionRequest
from runtime.operation_loop_bridge import bridge_operation_result
from runtime.operation_runner import OperationDefinition


def make_planned():
    operation = OperationDefinition(
        operation_id="R0082",
        base_ref="main",
        scope="implementation/operation",
    )
    request = ExecutionRequest(operation_id="R0082", execution_id="exec-1")
    return plan_execution_request(request, operation)


def test_operation_loop_bridge_preserves_planned_identity():
    planned = make_planned()
    boundary = bridge_operation_result(planned, "observed")

    assert boundary.identity == ("R0082", "exec-1")
    assert boundary.result.outcome == "observed"


def test_operation_loop_bridge_produces_distinct_result_for_distinct_execution():
    first = make_planned()
    second = first.__class__(
        request=ExecutionRequest(operation_id="R0082", execution_id="exec-2"),
        plan=first.plan,
    )

    first_boundary = bridge_operation_result(first, "observed")
    second_boundary = bridge_operation_result(second, "observed")

    assert first_boundary.identity != second_boundary.identity
    assert first_boundary.result is not second_boundary.result


def test_operation_loop_bridge_does_not_execute():
    planned = make_planned()
    bridge = bridge_operation_result(planned, "observed")

    assert not hasattr(bridge, "execute")
