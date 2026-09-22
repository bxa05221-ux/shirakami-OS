"""Immutable Evidence records emitted by the bounded Background Runner."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from runtime.background_runner import RunnerEvent


@dataclass(frozen=True)
class RunnerEvidence:
    """Immutable execution evidence preserving Runner identity."""

    event: str
    protocol_identity: str
    activation_identity: str
    approval_identity: str
    run_identity: str
    iteration: int
    runner_state: str

    @classmethod
    def from_event(cls, event: "RunnerEvent") -> "RunnerEvidence":
        return cls(
            event=event.event,
            protocol_identity=event.protocol_identity,
            activation_identity=event.activation_identity,
            approval_identity=event.approval_identity,
            run_identity=event.run_identity,
            iteration=event.iteration,
            runner_state=event.runner_state.value,
        )
