"""Minimal execution-authority boundary for Shirakami OS operations."""

from .operation_result import OperationResult
from .planned_execution import PlannedExecution


class OperationExecutor:
    """Execute one planned operation within the Runtime boundary.

    The executor owns only execution authority. It does not define Protocol
    semantics, mutate Landscape/Evidence, or evaluate AI/model quality.
    """

    def execute(self, planned: PlannedExecution, outcome: str) -> OperationResult:
        """Return the observable result identity for one planned execution."""
        return OperationResult(
            operation_id=planned.identity[0],
            execution_id=planned.identity[1],
            outcome=outcome,
        )
