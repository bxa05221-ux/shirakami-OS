"""Minimal first Landscape observation protocol: ``チューリップ``.

This is deliberately small. The protocol does not add botanical knowledge,
predict meaning, or choose a destination. It turns a human-provided word into
an observable Landscape transition and records the next thing worth observing.
"""

from typing import Any

from .prototype import ExecutionContext, Transition


TULIP_PROTOCOL_ID = "example.landscape.tulip"


def tulip_protocol(context: ExecutionContext) -> Transition:
    """Record ``チューリップ`` as the starting point of a small observation journey."""
    subject: Any = context.input.get("subject", "チューリップ")
    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("subject must be a non-empty string")

    return Transition(
        kind="landscape.observation.started",
        data={
            "changed": True,
            "subject": subject,
            "observation": "human_provided_subject",
            "next_observation": "look_again_from_another_distance_or_context",
            "projection": "none",
        },
    )


__all__ = ["TULIP_PROTOCOL_ID", "tulip_protocol"]
