"""Minimal operation runner boundary for Shirakami OS β1.0."""

from dataclasses import dataclass
from typing import Any, Mapping


FORBIDDEN_SCOPE = frozenset(
    {
        "new theory",
        "new Protocol semantics",
        "Landscape schema redesign",
        "Adapter contract change",
        "Renderer contract change",
        "AI/model quality evaluation",
    }
)


@dataclass(frozen=True)
class OperationDefinition:
    """Declarative description of one operational observation."""

    operation_id: str
    base_ref: str
    scope: str
    verification_gate: str = "test-runtime"


@dataclass(frozen=True)
class OperationPlan:
    """Validated execution plan; it does not mutate the repository."""

    operation_id: str
    base_ref: str
    verification_gate: str
    steps: tuple[str, ...]


def plan_operation(
    operation: OperationDefinition,
    metadata: Mapping[str, Any] | None = None,
) -> OperationPlan:
    """Validate an operation definition and return its deterministic plan."""
    del metadata

    if not operation.operation_id:
        raise ValueError("operation_id is required")
    if not operation.base_ref:
        raise ValueError("base_ref is required")
    if operation.scope in FORBIDDEN_SCOPE:
        raise ValueError(f"forbidden operation scope: {operation.scope}")
    if operation.verification_gate != "test-runtime":
        raise ValueError("unsupported verification gate")

    return OperationPlan(
        operation_id=operation.operation_id,
        base_ref=operation.base_ref,
        verification_gate=operation.verification_gate,
        steps=(
            "run-test-runtime",
            "create-artifact",
            "create-protected-pr",
        ),
    )
