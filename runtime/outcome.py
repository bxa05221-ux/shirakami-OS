"""Minimal observed-outcome boundary for Shirakami OS.

A human choice is not an outcome. An outcome is an explicitly supplied
observation of what happened after that choice. Only the Runtime transition
created from that observation can become Landscape Evidence.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from .choice import HandleChoice
from .handle import Handle
from .prototype import Transition


@dataclass(frozen=True)
class HandleOutcome:
    """Immutable observation of an actual result following a Handle choice."""

    handle_id: str
    choice_actor: str
    observed: Mapping[str, Any]


def observe_handle_outcome(
    choice: HandleChoice,
    observed: Mapping[str, Any],
) -> HandleOutcome:
    """Record an explicitly observed outcome without mutating Landscape."""
    if not isinstance(choice, HandleChoice):
        raise TypeError("choice must be a HandleChoice")
    if not isinstance(observed, Mapping):
        raise TypeError("observed must be a mapping")
    return HandleOutcome(
        handle_id=choice.handle_id,
        choice_actor=choice.actor,
        observed=dict(observed),
    )


def outcome_transition(outcome: HandleOutcome) -> Transition:
    """Convert an observed outcome into an explicit Landscape transition."""
    if not isinstance(outcome, HandleOutcome):
        raise TypeError("outcome must be a HandleOutcome")
    data = dict(outcome.observed)
    data.update(
        {
            "handle_id": outcome.handle_id,
            "choice_actor": outcome.choice_actor,
            "changed": True,
        }
    )
    return Transition(kind="landscape.handle.outcome", data=data)


OUTCOME_FORBIDDEN_OPERATIONS = frozenset(
    {
        "infer_outcome",
        "declare_success",
        "choose_values",
        "choose_faith",
        "make_decision",
        "mutate_landscape",
    }
)
