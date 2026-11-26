"""Read-only, JSON-compatible review of a ThreadRPG Cultural Trajectory turn.

This is a presentation projection only. It never resolves Evidence IDs,
promotes interpretations, or changes the originating AATS Thread.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

from runtime.threadrpg_cultural_trajectory import ThreadRPGCulturalTurn


def cultural_trajectory_review(turn: ThreadRPGCulturalTurn) -> dict[str, Any]:
    """Return detached, JSON-compatible source-to-interpretation review data."""
    if not isinstance(turn, ThreadRPGCulturalTurn):
        raise TypeError("turn must be a ThreadRPGCulturalTurn")

    if len(turn.sparks) != len(turn.oppai_observations):
        raise ValueError("spark/observation count mismatch")

    current = turn.revisited_trajectory or turn.trajectory
    original = turn.trajectory.document
    return {
        "status": "candidate_only",
        "evidence_resolution": "not_implemented",
        "posts": [
            {
                "source_ref": spark["source_ref"],
                "original_text": observation.raw_input,
                "spark_id": spark["id"],
            }
            for spark, observation in zip(turn.sparks, turn.oppai_observations)
        ],
        "relations": deepcopy(list(current.relations)),
        "trajectories": deepcopy(original["trajectories"]),
        "revisit_relations": [
            deepcopy(relation)
            for relation in current.relations
            if relation["revisits"]
        ],
        "verification": "unverified",
    }
