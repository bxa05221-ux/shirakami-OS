"""Minimal multi-handle boundary for Shirakami OS.

Multiple views may be offered side by side. The Runtime does not rank them
or choose one for the human; selection remains an explicit human action.
"""

from dataclasses import dataclass
from typing import Mapping, Sequence

from .handle import Handle, offer_handle
from .observation import ObservationView


@dataclass(frozen=True)
class HandleSet:
    """An immutable set of non-directive handles offered for human choice."""

    handles: tuple[Handle, ...]


def offer_handles(
    views: Sequence[ObservationView],
    *,
    labels: Mapping[str, str] | None = None,
) -> HandleSet:
    """Offer several explicit observation views without ranking or choosing.

    Each view becomes one Handle. Handle IDs are derived from lens names, so
    duplicate lenses are rejected rather than silently making one choice
    ambiguous.
    """
    handles = tuple(
        offer_handle(view, label=(labels or {}).get(view.lens))
        for view in views
    )
    ids = [handle.id for handle in handles]
    if len(ids) != len(set(ids)):
        raise ValueError("handle lenses must be unique")
    return HandleSet(handles=handles)


def select_handle(handle_set: HandleSet, handle_id: str) -> Handle:
    """Return an explicitly requested Handle; never select implicitly."""
    if not isinstance(handle_set, HandleSet):
        raise TypeError("handle_set must be a HandleSet")
    if not isinstance(handle_id, str) or not handle_id.strip():
        raise ValueError("handle_id must be a non-empty string")
    for handle in handle_set.handles:
        if handle.id == handle_id:
            return handle
    raise KeyError(handle_id)
