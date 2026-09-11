from runtime.execution_request import ExecutionRequest
from runtime.operation_executor import OperationExecutor
from runtime.operation_replay import execution_artifact, execution_branch
from runtime.operation_runner import OperationDefinition, plan_operation
from runtime.planned_execution import PlannedExecution


def _planned(execution_id: str) -> PlannedExecution:
    operation = OperationDefinition(
        operation_id="R0095",
        base_ref="main",
        scope="operation replay boundary verification",
    )
    plan = plan_operation(operation)
    request = ExecutionRequest("R0095", execution_id)
    return PlannedExecution(request=request, plan=plan)


def test_actual_executor_result_reaches_replay_addresses():
    executor = OperationExecutor()

    first = executor.execute(_planned("exec-001"), "verified")
    second = executor.execute(_planned("exec-002"), "verified")

    assert first.identity == ("R0095", "exec-001")
    assert second.identity == ("R0095", "exec-002")
    assert execution_branch(*first.identity) != execution_branch(*second.identity)
    assert execution_artifact(*first.identity) != execution_artifact(*second.identity)


def test_actual_executor_outcome_does_not_change_replay_address():
    executor = OperationExecutor()

    verified = executor.execute(_planned("exec-001"), "verified")
    observed = executor.execute(_planned("exec-001"), "observed")

    assert verified.identity == observed.identity
    assert execution_branch(*verified.identity) == execution_branch(*observed.identity)
    assert execution_artifact(*verified.identity) == execution_artifact(*observed.identity)
