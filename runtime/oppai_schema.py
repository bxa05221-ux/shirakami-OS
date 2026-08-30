"""OPPAI Schema: minimal human-input normalization boundary.

Operating Prompt Protocol for AI Schema

This module intentionally stays dependency-light. It does not call an LLM and
it does not decide what the user *really* means. It preserves raw language,
tracks explicit corrections, separates interaction signals from factual status,
and emits a bounded canonical prompt candidate for a downstream AI adapter.
"""

from dataclasses import dataclass
import re
from typing import Any, Mapping


_CORRECTION_MARKERS = ("いや", "違う", "ちがう", "そうじゃない", "訂正", "rather", "no,", "not that")
_AFFIRMATION_MARKERS = ("いい", "良い", "最高", "面白い", "すごい", "素晴らしい", "great", "good", "excellent")


@dataclass(frozen=True)
class OppaiObservation:
    """Inspectable result of one OPPAI preprocessing pass."""

    raw_input: str
    segments: tuple[str, ...]
    corrections: tuple[str, ...]
    interaction_signals: tuple[str, ...]
    unresolved: tuple[str, ...]
    canonical_prompt: str
    confidence: str


def _segments(text: str) -> tuple[str, ...]:
    parts = re.split(r"(?<=[。！？!?])\s*|\n+", text.strip())
    return tuple(part.strip() for part in parts if part.strip())


def _is_correction(segment: str) -> bool:
    normalized = segment.strip().lower()
    return any(normalized.startswith(marker.lower()) for marker in _CORRECTION_MARKERS)


def _signals(segments: tuple[str, ...]) -> tuple[str, ...]:
    found: list[str] = []
    for segment in segments:
        lower = segment.lower()
        if any(marker.lower() in lower for marker in _AFFIRMATION_MARKERS):
            found.append("positive_interaction")
    return tuple(dict.fromkeys(found))


def _unresolved(segments: tuple[str, ...]) -> tuple[str, ...]:
    found: list[str] = []
    for segment in segments:
        if "？" in segment or "?" in segment:
            found.append(segment)
    return tuple(found)


def normalize(text: str, context: Mapping[str, Any] | None = None) -> OppaiObservation:
    """Normalize natural human input without forcing premature semantic closure.

    ``context`` is accepted for forward compatibility but is not interpreted in
    this minimal slice. The first implementation does not infer hidden intent.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")

    raw = text
    segments = _segments(raw)
    corrections = tuple(segment for segment in segments if _is_correction(segment))
    signals = _signals(segments)
    unresolved = _unresolved(segments)

    # Preserve the complete conversational sequence. Corrections are evidence
    # about interpretation state, not instructions to erase earlier context.
    canonical = "\n".join(segments)
    confidence = "provisional" if corrections or unresolved else "observed"

    return OppaiObservation(
        raw_input=raw,
        segments=segments,
        corrections=corrections,
        interaction_signals=signals,
        unresolved=unresolved,
        canonical_prompt=canonical,
        confidence=confidence,
    )


def to_dict(observation: OppaiObservation) -> dict[str, Any]:
    """Serialize an observation for Runtime/API boundaries."""
    return {
        "raw_input": observation.raw_input,
        "segments": list(observation.segments),
        "corrections": list(observation.corrections),
        "interaction_signals": list(observation.interaction_signals),
        "unresolved": list(observation.unresolved),
        "canonical_prompt": observation.canonical_prompt,
        "confidence": observation.confidence,
    }
