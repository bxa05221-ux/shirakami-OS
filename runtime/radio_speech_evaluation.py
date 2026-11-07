"""Narrow, offline regression checks for Shirakami Radio draft speech.

These checks are deliberately lexical heuristics.  They flag a small set of
known-risk phrases and shared scene markers in fixture output; they cannot
establish naturalness, factuality, or compliance of arbitrary model output.
Their result is advisory test data only: it is not Evidence, authority, or a
Reality mutation.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Mapping, Sequence


_SCENE_MARKERS: Mapping[str, tuple[str, ...]] = {
    "station": ("駅", "ホーム", "改札", "電車"),
    "rain": ("雨", "傘", "水たまり"),
    "coffee": ("コーヒー", "喫茶", "マグカップ"),
    "garden": ("庭", "植物", "花", "葉っぱ"),
    "book": ("本", "ページ", "図書館"),
}
_ADVISORY_OR_ANALYTICAL_MARKERS = (
    "すべき",
    "したほうが",
    "おすすめ",
    "助言",
    "分析すると",
    "心理",
    "あなたは",
)
_SEMANTIC_BRIDGE_MARKERS = (
    "どちらも",
    "共通して",
    "だからこそ",
    "教えてくれ",
    "つながって",
    "同じこと",
)
_EXPLANATORY_MARKERS = ("つまり", "要するに", "まとめると", "理由は", "結論として")
_PERFORMATIVE_EMOTION_MARKERS = ("すごくすごく", "最高すぎ", "！！", "！！！")

# These are script-review estimates, not measurements of a renderer or voice.
_JAPANESE_CHARS_PER_SECOND = 5.0
_LISTENER_MIN_CHARS = 100
_LISTENER_MAX_CHARS = 250
_PERSONALITY_MIN_SECONDS = 15
_PERSONALITY_MAX_SECONDS = 40


@dataclass(frozen=True)
class RadioSpeechEvaluation:
    """Advisory findings from limited fixture-oriented lexical checks."""

    duplicate_landscape_pairs: tuple[tuple[int, int, str], ...]
    personality_restriction_hits: tuple[str, ...]
    semantic_bridge_hits: tuple[str, ...]
    listener_length_violations: tuple[tuple[int, int], ...] = ()
    personality_explanation_hits: tuple[str, ...] = ()
    performative_emotion_hits: tuple[str, ...] = ()
    personality_duration_estimates: tuple[float, ...] = ()
    personality_duration_violations: tuple[tuple[int, float], ...] = ()
    limitation: str = (
        "Lexical and character-count regression heuristics only; this does not "
        "guarantee naturalness, speech quality, or protocol compliance. Duration "
        "is an approximate text-only estimate (5 Japanese characters/second), not "
        "a measurement of actual speaking rate or voice quality."
    )


def _scene_categories(text: str) -> set[str]:
    return {
        category
        for category, markers in _SCENE_MARKERS.items()
        if any(marker in text for marker in markers)
    }


def _script_character_count(text: str) -> int:
    """Count visible script characters for stable fixture-only length checks."""
    return len("".join(text.split()))


def evaluate_radio_speech(
    listener_posts: Sequence[str], personality_comments: Sequence[str]
) -> RadioSpeechEvaluation:
    """Inspect supplied draft strings without calling models or mutating state."""
    duplicate_pairs: list[tuple[int, int, str]] = []
    for (left_index, left), (right_index, right) in combinations(enumerate(listener_posts), 2):
        for category in sorted(_scene_categories(left) & _scene_categories(right)):
            duplicate_pairs.append((left_index, right_index, category))

    personality_hits = tuple(
        comment
        for comment in personality_comments
        if any(marker in comment for marker in _ADVISORY_OR_ANALYTICAL_MARKERS)
    )
    bridge_hits = tuple(
        comment
        for comment in personality_comments
        if any(marker in comment for marker in _SEMANTIC_BRIDGE_MARKERS)
    )
    listener_length_violations = tuple(
        (index, character_count)
        for index, post in enumerate(listener_posts)
        if not (_LISTENER_MIN_CHARS <= (character_count := _script_character_count(post)) <= _LISTENER_MAX_CHARS)
    )
    explanation_hits = tuple(
        comment
        for comment in personality_comments
        if any(marker in comment for marker in _EXPLANATORY_MARKERS)
    )
    emotion_hits = tuple(
        comment
        for comment in personality_comments
        if any(marker in comment for marker in _PERFORMATIVE_EMOTION_MARKERS)
    )
    duration_estimates = tuple(
        round(_script_character_count(comment) / _JAPANESE_CHARS_PER_SECOND, 1)
        for comment in personality_comments
    )
    duration_violations = tuple(
        (index, seconds)
        for index, seconds in enumerate(duration_estimates)
        if not (_PERSONALITY_MIN_SECONDS <= seconds <= _PERSONALITY_MAX_SECONDS)
    )
    return RadioSpeechEvaluation(
        duplicate_landscape_pairs=tuple(duplicate_pairs),
        personality_restriction_hits=personality_hits,
        semantic_bridge_hits=bridge_hits,
        listener_length_violations=listener_length_violations,
        personality_explanation_hits=explanation_hits,
        performative_emotion_hits=emotion_hits,
        personality_duration_estimates=duration_estimates,
        personality_duration_violations=duration_violations,
    )
