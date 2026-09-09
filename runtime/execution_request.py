"""Explicit execution-request boundary for Shirakami OS operations."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionRequest:
    """Request one execution instance without executing it."""

    operation_id: str
    execution_id: str

    def __post_init__(self) -> None:
        if not self.operation_id:
            raise ValueError("operation_id is required")
        if not self.execution_id:
            raise ValueError("execution_id is required")

    @property
    def identity(self) -> tuple[str, str]:
        """Return the stable request identity pair."""
        return (self.operation_id, self.execution_id)
