"""Protocol input boundary for Context Snapshots."""
from __future__ import annotations

from dataclasses import dataclass

from .context_boundary import ContextSnapshot


@dataclass(frozen=True)
class ProtocolInput:
    context_id: str
    parent_landscape_ref: str
    source_refs: tuple[object, ...]
    unresolved_questions: tuple[str, ...]
    requested_context: str | None = None


def create_protocol_input(context: ContextSnapshot) -> ProtocolInput:
    """Pass a Context Snapshot through without semantic interpretation."""
    if not context.context_id:
        raise ValueError("context_id is required")
    if not context.parent_landscape_ref:
        raise ValueError("parent_landscape_ref is required")

    return ProtocolInput(
        context_id=context.context_id,
        parent_landscape_ref=context.parent_landscape_ref,
        source_refs=context.source_refs,
        unresolved_questions=context.unresolved_questions,
        requested_context=context.requested_context,
    )
