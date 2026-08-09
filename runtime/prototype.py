"""Shirakami Runtime β0.1 minimal vertical slice.

Protocol -> Context -> Execution -> Observable Transition -> Result

This prototype intentionally avoids external dependencies and backend-specific
behavior. It is an executable boundary test, not the final Runtime architecture.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Mapping


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


Protocol = Callable[[ExecutionContext], Transition]


class Runtime:
    """Minimal replaceable Runtime boundary for β0.1."""

    def execute(
        self,
        protocol_id: str,
        protocol: Protocol,
        input_data: Mapping[str, Any] | None = None,
    ) -> ExecutionResult:
        context = ExecutionContext(
            protocol_id=protocol_id,
            input=dict(input_data or {}),
        )

        transition = protocol(context)

        return ExecutionResult(
            status="completed",
            protocol_id=protocol_id,
            transition=transition,
            signals=("execution.completed", "transition.observed"),
        )


# Deterministic Protocol used only for the minimal vertical-slice demonstration.
def example_protocol(context: ExecutionContext) -> Transition:
    return Transition(
        kind="example.transition",
        data={
            "protocol_id": context.protocol_id,
            "input": dict(context.input),
            "changed": True,
        },
    )


if __name__ == "__main__":
    runtime = Runtime()
    result = runtime.execute(
        "example.protocol",
        example_protocol,
        {"message": "hello landscape"},
    )
    print(result)
