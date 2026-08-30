"""Minimal OPPAI boundary helpers.

This module deliberately does not attempt to infer a hidden truth. It keeps
raw user input separate from runtime observations and returns a small,
provider-neutral envelope for the adapter layer.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class OppaiEnvelope:
    raw_input: str
    context: dict[str, Any] = field(default_factory=dict)
    intent: str | None = None
    clarification_required: bool = False


def listen(input_text: str, context: dict[str, Any] | None = None) -> OppaiEnvelope:
    """Capture natural input without forcing a prompt format."""
    return OppaiEnvelope(raw_input=input_text, context=dict(context or {}))


def needs_clarification(envelope: OppaiEnvelope) -> bool:
    """Conservative placeholder: ambiguity must be explicitly detected later.

    v0.1 does not guess. Callers may mark clarification_required after their
    own domain/runtime checks.
    """
    return envelope.clarification_required
