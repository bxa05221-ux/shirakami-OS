"""Planned execution identity boundary for Shirakami OS operations."""

from dataclasses import dataclass

from .execution_request import ExecutionRequest
from .operation_runner import OperationPlan


@dataclass(frozen=True)
class PlannedExecution:
    """Bind one execution request to its validated operation plan."""

    request: ExecutionRequest
    plan: OperationPlan

    def __post_init__(self) -> None:
        if self.request.operation_id != self.plan.operation_id:
            raise ValueError("operation_id does not match operation plan")

    @property
    def identity(self) -> tuple[str, str]:
        """Return the execution identity inherited from the request."""
        return self.request.identity
