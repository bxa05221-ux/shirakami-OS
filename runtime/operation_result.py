"""Immutable result record for one Shirakami OS operation execution."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OperationResult:
    """Observable execution result identified independently of the operation."""

    operation_id: str
    execution_id: str
    outcome: str
    verification_gate: str = "test-runtime"

    def __post_init__(self) -> None:
        if not self.operation_id:
            raise ValueError("operation_id is required")
        if not self.execution_id:
            raise ValueError("execution_id is required")
        if not self.outcome:
            raise ValueError("outcome is required")
        if self.verification_gate != "test-runtime":
            raise ValueError("unsupported verification gate")

    @property
    def identity(self) -> tuple[str, str]:
        """Return the stable operation/execution identity pair."""
        return self.operation_id, self.execution_id

    def as_record(self) -> dict[str, str]:
        """Return a plain value record for observation serialization."""
        return {
            "operation_id": self.operation_id,
            "execution_id": self.execution_id,
            "outcome": self.outcome,
            "verification_gate": self.verification_gate,
        }
