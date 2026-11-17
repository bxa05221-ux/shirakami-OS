"""Small, local-only bridge from a ThreadRPG-like turn to Cultural Trajectory.

The bridge observes supplied messages through OPPAI and preserves their text as
Spark candidates.  It records one deliberately unverified Relation candidate;
it neither sends a log anywhere nor selects a Runtime route, creates Evidence,
or approves a Human Gate decision.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from runtime.cultural_trajectory import CulturalTrajectory
from runtime.oppai_schema import OppaiObservation, normalize


@dataclass(frozen=True)
class ThreadRPGCulturalTurn:
    """Detached outputs from one local, synthetic-or-caller-owned thread turn."""

    sparks: tuple[Mapping[str, Any], ...]
    oppai_observations: tuple[OppaiObservation, ...]
    relation_candidate: Mapping[str, Any]
    trajectory: CulturalTrajectory
    revisited_trajectory: CulturalTrajectory | None = None

    def revisit(self, relation_type: str) -> Mapping[str, Any]:
        """Append a new unverified interpretation that explicitly revisits the candidate."""
        if not isinstance(relation_type, str) or not relation_type:
            raise ValueError("relation_type must be a non-empty string")
        relation = {
            "id": f"{self.relation_candidate['id']}-REVISIT-001",
            "from": self.relation_candidate["from"],
            "to": self.relation_candidate["to"],
            "type": relation_type,
            "assertion": {"kind": "interpretation", "author": "anonymous-adapter", "verification": "unverified"},
            "provenance": {
                "source_refs": list(self.relation_candidate["provenance"]["source_refs"]),
                "evidence_ids": list(self.relation_candidate["provenance"]["evidence_ids"]),
                "witness_ids": [],
            },
            "revisits": [self.relation_candidate["id"]],
        }
        object.__setattr__(self, "revisited_trajectory", self.trajectory.append_relation(relation))
        return deepcopy(relation)


def observe_threadrpg_turn(messages: Sequence[Mapping[str, Any]]) -> ThreadRPGCulturalTurn:
    """Create candidate-only Cultural Trajectory data from a two-or-more-message turn."""
    if len(messages) < 2:
        raise ValueError("messages must contain at least two posts")

    sparks: list[dict[str, Any]] = []
    observations: list[OppaiObservation] = []
    for index, message in enumerate(messages, start=1):
        if not isinstance(message, Mapping):
            raise ValueError("each message must be a mapping")
        source_ref = message.get("id")
        text = message.get("text")
        if not isinstance(source_ref, str) or not source_ref:
            raise ValueError("each message id must be a non-empty string")
        observation = normalize(text)
        sparks.append({"id": f"SP-{index:03d}", "type": "spark", "text": observation.raw_input, "source_ref": source_ref})
        observations.append(observation)

    thread_ref = sparks[0]["source_ref"].split(":", 1)[0]
    relation = {
        "id": "REL-001",
        "from": sparks[0]["id"],
        "to": sparks[1]["id"],
        "type": "possible_response",
        "assertion": {"kind": "interpretation", "author": "anonymous-adapter", "verification": "unverified"},
        "provenance": {
            "source_refs": [sparks[0]["source_ref"], sparks[1]["source_ref"]],
            "evidence_ids": [f"evidence:{thread_ref}"],
            "witness_ids": [],
        },
        "revisits": [],
    }
    document = {
        "cultural_trajectory": {
            "schema_version": "0.1",
            "objects": sparks,
            "relations": [relation],
            "trajectories": [{"id": f"TRJ-{thread_ref}", "kind": "observed", "relation_ids": [relation["id"]], "source_refs": [thread_ref], "verification": "unverified"}],
            "preservation": {"append_only": True, "allow_conflicting_relations": True, "overwrite_original": False, "automatic_promotion": False},
        }
    }
    return ThreadRPGCulturalTurn(
        sparks=tuple(deepcopy(sparks)),
        oppai_observations=tuple(observations),
        relation_candidate=deepcopy(relation),
        trajectory=CulturalTrajectory.from_mapping(document),
    )
