"""Immutable result identity for Shirakami OS operation executions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OperationResult:
    """Observable result identity for one execution instance."""

    operation_id: str
    execution_id: str
    outcome: str

    def __post_init__(self) -> None:
        if not self.operation_id:
            raise ValueError("operation_id is required")
        if not self.execution_id:
            raise ValueError("execution_id is required")
        if not self.outcome:
            raise ValueError("outcome is required")

    @property
    def identity(self) -> tuple[str, str]:
        """Return the stable operation/execution identity pair."""
        return (self.operation_id, self.execution_id)
