"""Execution boundary for planned Shirakami OS operation executions."""

from dataclasses import dataclass

from .operation_result import OperationResult
from .planned_execution import PlannedExecution


@dataclass(frozen=True)
class ExecutionBoundary:
    """Bind one planned execution to its observable operation result."""

    planned: PlannedExecution
    result: OperationResult

    def __post_init__(self) -> None:
        if self.result.identity != self.planned.identity:
            raise ValueError("operation execution identity does not match planned execution")

    @property
    def identity(self) -> tuple[str, str]:
        """Return the execution identity shared by plan and result."""
        return self.planned.identity
