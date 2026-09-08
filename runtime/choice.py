"""Minimal human-choice boundary for Shirakami OS.

A choice records that a human selected an offered Handle. Selection is not
itself a Landscape change; an actual outcome must be observed separately.
"""

from dataclasses import dataclass

from .handle import Handle


@dataclass(frozen=True)
class HandleChoice:
    """Immutable record of a human selecting a Handle."""

    handle_id: str
    actor: str = "human"


def choose_handle(handle: Handle, *, actor: str = "human") -> HandleChoice:
    """Record a human choice without opening, executing, or mutating anything."""
    if not isinstance(handle, Handle):
        raise TypeError("handle must be a Handle")
    if not isinstance(actor, str) or not actor.strip():
        raise ValueError("actor must be a non-empty string")
    return HandleChoice(handle_id=handle.id, actor=actor)
