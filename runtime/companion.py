"""Minimal companion boundary for Shirakami OS.

A Companion speaks alongside a human without taking over the route,
choosing values, or claiming to know what the human should do.
"""
from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class CompanionLine:
    """One offered line from a companion."""

    text: str
    tone: str = "friendly"
    context: Mapping[str, Any] | None = None


def offer_companion_line(
    text: str,
    *,
    tone: str = "friendly",
    context: Mapping[str, Any] | None = None,
) -> CompanionLine:
    """Offer a companion line without turning it into an instruction."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")
    if not isinstance(tone, str) or not tone.strip():
        raise ValueError("tone must be a non-empty string")
    if context is not None and not isinstance(context, Mapping):
        raise TypeError("context must be a mapping or None")
    return CompanionLine(text=text, tone=tone, context=dict(context or {}))


COMPANION_FORBIDDEN_OPERATIONS = frozenset(
    {
        "choose_destination",
        "choose_values",
        "choose_faith",
        "make_decision",
        "claim_outcome",
        "mutate_landscape",
    }
)
