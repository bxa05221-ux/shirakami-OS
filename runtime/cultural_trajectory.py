"""Deterministic, append-only Cultural Trajectory PoC boundary.

This module deliberately stores no state outside the supplied YAML document.
It does not infer cultural meaning, promote an interpretation, execute a
Protocol, or issue a Human Gate approval.  Existing OPPAI, RouteMap, Human
Gate, and Evidence boundaries remain the owners of those responsibilities.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml


class CulturalTrajectoryError(ValueError):
    """Raised when a Cultural Trajectory document is structurally invalid."""


def _mapping(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise CulturalTrajectoryError(f"{label} must be a mapping")
    return value


def _non_empty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise CulturalTrajectoryError(f"{label} must be a non-empty string")
    return value


def _string_list(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise CulturalTrajectoryError(f"{label} must be a list of non-empty strings")
    return tuple(value)


@dataclass(frozen=True)
class CulturalTrajectory:
    """Validated YAML data with append-only relation history operations."""

    document: Mapping[str, Any]

    @classmethod
    def from_yaml(cls, path: str | Path) -> "CulturalTrajectory":
        with Path(path).open(encoding="utf-8") as stream:
            loaded = yaml.safe_load(stream)
        return cls.from_mapping(loaded)

    @classmethod
    def from_mapping(cls, value: object) -> "CulturalTrajectory":
        root = _mapping(value, "document")
        payload = _mapping(root.get("cultural_trajectory"), "cultural_trajectory")
        cls._validate(payload)
        # Copy the outer containers so caller mutation cannot alter this view.
        copied = dict(payload)
        copied["objects"] = tuple(dict(item) for item in payload["objects"])
        copied["relations"] = tuple(dict(item) for item in payload["relations"])
        copied["trajectories"] = tuple(dict(item) for item in payload["trajectories"])
        return cls(document=copied)

    @staticmethod
    def _validate(payload: Mapping[str, Any]) -> None:
        _non_empty_string(payload.get("schema_version"), "schema_version")
        preservation = _mapping(payload.get("preservation"), "preservation")
        if preservation.get("append_only") is not True:
            raise CulturalTrajectoryError("preservation.append_only must be true")
        if preservation.get("allow_conflicting_relations") is not True:
            raise CulturalTrajectoryError("preservation.allow_conflicting_relations must be true")
        if preservation.get("overwrite_original") is not False:
            raise CulturalTrajectoryError("preservation.overwrite_original must be false")
        if preservation.get("automatic_promotion") is not False:
            raise CulturalTrajectoryError("preservation.automatic_promotion must be false")

        objects = payload.get("objects")
        relations = payload.get("relations")
        trajectories = payload.get("trajectories")
        if not isinstance(objects, list) or not isinstance(relations, list) or not isinstance(trajectories, list):
            raise CulturalTrajectoryError("objects, relations, and trajectories must be lists")

        object_ids: set[str] = set()
        for index, item in enumerate(objects):
            item = _mapping(item, f"objects[{index}]")
            identifier = _non_empty_string(item.get("id"), f"objects[{index}].id")
            _non_empty_string(item.get("type"), f"objects[{index}].type")
            if identifier in object_ids:
                raise CulturalTrajectoryError(f"duplicate object id: {identifier}")
            object_ids.add(identifier)

        relation_ids: set[str] = set()
        for index, item in enumerate(relations):
            CulturalTrajectory._validate_relation(item, index, object_ids, relation_ids)
            relation_ids.add(item["id"])

        trajectory_ids: set[str] = set()
        for index, item in enumerate(trajectories):
            item = _mapping(item, f"trajectories[{index}]")
            identifier = _non_empty_string(item.get("id"), f"trajectories[{index}].id")
            if identifier in trajectory_ids:
                raise CulturalTrajectoryError(f"duplicate trajectory id: {identifier}")
            trajectory_ids.add(identifier)
            _non_empty_string(item.get("kind"), f"trajectories[{index}].kind")
            for relation_id in _string_list(item.get("relation_ids"), f"trajectories[{index}].relation_ids"):
                if relation_id not in relation_ids:
                    raise CulturalTrajectoryError(f"trajectory references unknown relation: {relation_id}")
            _string_list(item.get("source_refs"), f"trajectories[{index}].source_refs")
            _non_empty_string(item.get("verification"), f"trajectories[{index}].verification")

    @staticmethod
    def _validate_relation(item: object, index: int, object_ids: set[str], prior_ids: set[str]) -> None:
        relation = _mapping(item, f"relations[{index}]")
        identifier = _non_empty_string(relation.get("id"), f"relations[{index}].id")
        if identifier in prior_ids:
            raise CulturalTrajectoryError(f"duplicate relation id: {identifier}")
        for endpoint in ("from", "to"):
            target = _non_empty_string(relation.get(endpoint), f"relations[{index}].{endpoint}")
            if target not in object_ids:
                raise CulturalTrajectoryError(f"relation references unknown object: {target}")
        _non_empty_string(relation.get("type"), f"relations[{index}].type")
        assertion = _mapping(relation.get("assertion"), f"relations[{index}].assertion")
        if assertion.get("kind") != "interpretation":
            raise CulturalTrajectoryError("relations must be explicitly marked as interpretations")
        _non_empty_string(assertion.get("author"), f"relations[{index}].assertion.author")
        if assertion.get("verification") != "unverified":
            raise CulturalTrajectoryError("interpretations must not be promoted by this PoC")
        provenance = _mapping(relation.get("provenance"), f"relations[{index}].provenance")
        _string_list(provenance.get("source_refs"), f"relations[{index}].provenance.source_refs")
        _string_list(provenance.get("evidence_ids"), f"relations[{index}].provenance.evidence_ids")
        _string_list(provenance.get("witness_ids"), f"relations[{index}].provenance.witness_ids")
        for revisit in _string_list(relation.get("revisits"), f"relations[{index}].revisits"):
            if revisit not in prior_ids:
                raise CulturalTrajectoryError(f"relation revisits unknown or future relation: {revisit}")

    @property
    def relations(self) -> tuple[Mapping[str, Any], ...]:
        return self.document["relations"]

    def append_relation(self, relation: Mapping[str, Any]) -> "CulturalTrajectory":
        """Return a new document; the original relation history is untouched."""
        object_ids = {item["id"] for item in self.document["objects"]}
        prior_ids = {item["id"] for item in self.relations}
        self._validate_relation(relation, len(prior_ids), object_ids, prior_ids)
        replacement = dict(self.document)
        replacement["relations"] = [dict(item) for item in self.relations] + [dict(relation)]
        replacement["objects"] = [dict(item) for item in self.document["objects"]]
        replacement["trajectories"] = [dict(item) for item in self.document["trajectories"]]
        return CulturalTrajectory.from_mapping({"cultural_trajectory": replacement})

    def reconstruct(self, trajectory_id: str) -> tuple[Mapping[str, Any], ...]:
        """Return the declared relation sequence without inferring a new path."""
        trajectory = next((item for item in self.document["trajectories"] if item["id"] == trajectory_id), None)
        if trajectory is None:
            raise CulturalTrajectoryError(f"unknown trajectory: {trajectory_id}")
        by_id = {item["id"]: item for item in self.relations}
        return tuple(by_id[relation_id] for relation_id in trajectory["relation_ids"])

    def human_gate_candidate(self, relation_id: str) -> dict[str, Any]:
        """Expose an interpretation as non-executable, non-authoritative input to Human Gate."""
        if relation_id not in {item["id"] for item in self.relations}:
            raise CulturalTrajectoryError(f"unknown relation: {relation_id}")
        return {
            "candidate_identity": f"cultural-relation:{relation_id}",
            "authority": False,
            "executable": False,
            "validation": True,
        }
