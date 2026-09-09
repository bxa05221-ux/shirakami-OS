"""Connect an execution request to the existing deterministic operation plan."""

from runtime.execution_request import ExecutionRequest
from runtime.operation_runner import OperationDefinition, OperationPlan, plan_operation


def plan_execution_request(
    request: ExecutionRequest,
    operation: OperationDefinition,
) -> OperationPlan:
    """Validate request identity against an operation and return its plan.

    This function plans only; it does not execute, mutate Landscape/Evidence,
    or grant execution authority.
    """
    if request.operation_id != operation.operation_id:
        raise ValueError("execution request operation_id does not match operation")

    return plan_operation(operation)
