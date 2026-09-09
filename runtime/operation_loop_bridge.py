"""Bridge a planned execution boundary to an existing observable result."""

from .execution_boundary import ExecutionBoundary
from .operation_result import OperationResult
from .planned_execution import PlannedExecution


def bridge_operation_result(
    planned: PlannedExecution,
    outcome: str,
) -> ExecutionBoundary:
    """Create an observable result for one planned execution.

    This bridge records only the execution identity and outcome. It does not
    execute an operation, mutate Landscape/Evidence, or grant authority.
    """
    result = OperationResult(
        operation_id=planned.operation_id,
        execution_id=planned.identity[1],
        outcome=outcome,
    )
    return ExecutionBoundary(planned=planned, result=result)
