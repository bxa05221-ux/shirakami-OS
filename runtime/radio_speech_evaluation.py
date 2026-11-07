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


@dataclass(frozen=True)
class RadioSpeechEvaluation:
    """Advisory findings from limited fixture-oriented lexical checks."""

    duplicate_landscape_pairs: tuple[tuple[int, int, str], ...]
    personality_restriction_hits: tuple[str, ...]
    semantic_bridge_hits: tuple[str, ...]
    limitation: str = (
        "Lexical regression heuristics only; this does not guarantee speech quality "
        "or protocol compliance."
    )


def _scene_categories(text: str) -> set[str]:
    return {
        category
        for category, markers in _SCENE_MARKERS.items()
        if any(marker in text for marker in markers)
    }


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
    return RadioSpeechEvaluation(
        duplicate_landscape_pairs=tuple(duplicate_pairs),
        personality_restriction_hits=personality_hits,
        semantic_bridge_hits=bridge_hits,
    )
