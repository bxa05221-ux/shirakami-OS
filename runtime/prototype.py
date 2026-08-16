"""Shirakami Runtime β0.1 minimal vertical slice.

Protocol -> Context -> Execution -> Observable Transition -> Result

This prototype intentionally avoids external dependencies and backend-specific
behavior. It is an executable boundary test, not the final Runtime architecture.
"""

from dataclasses import dataclass
from typing import Any, Callable, Mapping


@dataclass(frozen=True)
class ExecutionBudget:
    """Resource boundary for one Runtime execution."""

    max_steps: int = 1

    def validate(self) -> dict[str, str] | None:
        if not isinstance(self.max_steps, int) or self.max_steps < 1:
            return {
                "error_type": "InvalidExecutionBudget",
                "message": "max_steps must be an integer >= 1",
            }
        return None


@dataclass(frozen=True)
class ExecutionContext:
    """Bounded context for one Protocol execution."""

    protocol_id: str
    input: Mapping[str, Any]


@dataclass(frozen=True)
class Transition:
    """Observable Landscape-relevant transition produced by execution."""

    kind: str
    data: Mapping[str, Any]


@dataclass(frozen=True)
class ExecutionResult:
    """Inspectable result of one Runtime execution."""

    status: str
    protocol_id: str
    transition: Transition
    signals: tuple[str, ...] = ()
    steps: int = 0


Protocol = Callable[[ExecutionContext], Transition]


class Runtime:
    """Minimal replaceable Runtime boundary for β0.1."""

    def __init__(self, budget: ExecutionBudget | None = None) -> None:
        self.budget = budget or ExecutionBudget()

    def execute(
        self,
        protocol_id: str,
        protocol: Protocol,
        input_data: Mapping[str, Any] | None = None,
    ) -> ExecutionResult:
        budget_error = self.budget.validate()
        if budget_error is not None:
            return ExecutionResult(
                status="failed",
                protocol_id=protocol_id if isinstance(protocol_id, str) else "",
                transition=Transition(kind="execution.budget.invalid", data=budget_error),
                signals=("execution.invalid", "transition.observed"),
            )
        if self.budget.max_steps < 1:
            return ExecutionResult(
                status="failed",
                protocol_id=protocol_id if isinstance(protocol_id, str) else "",
                transition=Transition(
                    kind="execution.budget.exceeded",
                    data={"error_type": "ExecutionBudgetExceeded", "message": "execution step budget exhausted"},
                ),
                signals=("execution.budget.exceeded", "transition.observed"),
            )

        validation_error = self._validate_execution_input(protocol_id, protocol, input_data)
        if validation_error is not None:
            return ExecutionResult(
                status="failed",
                protocol_id=protocol_id if isinstance(protocol_id, str) else "",
                transition=Transition(kind="execution.invalid_input", data=validation_error),
                signals=("execution.invalid", "transition.observed"),
            )

        context = ExecutionContext(protocol_id=protocol_id, input=dict(input_data or {}))

        try:
            transition = protocol(context)
        except Exception as exc:
            return ExecutionResult(
                status="failed",
                protocol_id=protocol_id,
                transition=Transition(
                    kind="execution.failed",
                    data={"error_type": type(exc).__name__, "message": str(exc)},
                ),
                signals=("execution.failed", "transition.observed"),
                steps=1,
            )

        if not isinstance(transition, Transition):
            return ExecutionResult(
                status="failed",
                protocol_id=protocol_id,
                transition=Transition(
                    kind="execution.invalid_result",
                    data={
                        "error_type": "InvalidProtocolResult",
                        "message": "Protocol must return Transition",
                    },
                ),
                signals=("execution.invalid", "transition.observed"),
                steps=1,
            )

        return ExecutionResult(
            status="completed",
            protocol_id=protocol_id,
            transition=transition,
            signals=("execution.completed", "transition.observed"),
            steps=1,
        )

    @staticmethod
    def _validate_execution_input(
        protocol_id: str,
        protocol: Protocol,
        input_data: Mapping[str, Any] | None,
    ) -> dict[str, str] | None:
        if not isinstance(protocol_id, str) or not protocol_id.strip():
            return {"error_type": "InvalidProtocolId", "message": "protocol_id must be a non-empty string"}
        if not callable(protocol):
            return {"error_type": "InvalidProtocol", "message": "protocol must be callable"}
        if input_data is not None and not isinstance(input_data, Mapping):
            return {"error_type": "InvalidContextInput", "message": "input_data must be a mapping or None"}
        return None


def example_protocol(context: ExecutionContext) -> Transition:
    return Transition(
        kind="example.transition",
        data={"protocol_id": context.protocol_id, "input": dict(context.input), "changed": True},
    )


def failing_protocol(context: ExecutionContext) -> Transition:
    raise RuntimeError("intentional prototype failure")


if __name__ == "__main__":
    runtime = Runtime()
    result = runtime.execute("example.protocol", example_protocol, {"message": "hello landscape"})
    print(result)
