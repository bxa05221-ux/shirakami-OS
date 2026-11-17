from copy import deepcopy
from pathlib import Path

import pytest

from runtime.cultural_trajectory import CulturalTrajectory, CulturalTrajectoryError
from runtime.human_gate import process_human_gate
from runtime.oppai_schema import normalize
from runtime.route_map import RouteMap


FIXTURE = Path(__file__).parent / "fixtures" / "cultural_trajectory_v0_1.yaml"


def test_yaml_load_references_and_trajectory_reconstruction_are_deterministic():
    trajectory = CulturalTrajectory.from_yaml(FIXTURE)

    reconstructed = trajectory.reconstruct("TRJ-001")

    assert [relation["id"] for relation in reconstructed] == ["REL-001", "REL-002"]
    assert [relation["type"] for relation in reconstructed] == ["contradicts", "reinterprets"]


def test_conflicting_interpretation_appends_without_rewriting_history():
    original = CulturalTrajectory.from_yaml(FIXTURE)
    new_relation = {
        "id": "REL-003",
        "from": "SP-001",
        "to": "SP-002",
        "type": "resonates",
        "assertion": {"kind": "interpretation", "author": "another-anonymous", "verification": "unverified"},
        "provenance": {"source_refs": ["fixture:thread-001:post-001"], "evidence_ids": [], "witness_ids": []},
        "revisits": ["REL-001"],
    }

    revised = original.append_relation(new_relation)

    assert [item["id"] for item in original.relations] == ["REL-001", "REL-002"]
    assert [item["id"] for item in revised.relations] == ["REL-001", "REL-002", "REL-003"]
    assert revised.relations[-1]["type"] == "resonates"
    assert revised.relations[-1]["revisits"] == ("REL-001",) or revised.relations[-1]["revisits"] == ["REL-001"]


def test_nested_input_and_public_snapshots_cannot_mutate_saved_history():
    source = CulturalTrajectory.from_yaml(FIXTURE).document
    trajectory = CulturalTrajectory.from_mapping({"cultural_trajectory": source})

    source["relations"][0]["assertion"]["author"] = "changed-input"
    published_relation = trajectory.relations[0]
    published_relation["assertion"]["author"] = "changed-public-relation"
    published_document = trajectory.document
    published_document["relations"][0]["provenance"]["evidence_ids"].append("evidence:injected")
    reconstructed = trajectory.reconstruct("TRJ-001")
    reconstructed[0]["provenance"]["source_refs"].append("fixture:injected")

    saved = trajectory.relations[0]
    assert saved["assertion"]["author"] == "anonymous"
    assert saved["provenance"]["evidence_ids"] == ["evidence:observed-posts-001"]
    assert saved["provenance"]["source_refs"] == ["fixture:thread-001:post-001", "fixture:thread-001:post-002"]


def test_append_keeps_both_histories_and_the_relation_argument_immutable():
    original = CulturalTrajectory.from_yaml(FIXTURE)
    relation = {
        "id": "REL-003",
        "from": "SP-003",  # Cultural trajectories need not be Runtime-continuous paths.
        "to": "SP-001",
        "type": "resonates",
        "assertion": {"kind": "interpretation", "author": "another-anonymous", "verification": "unverified"},
        "provenance": {"source_refs": ["fixture:thread-001:post-003"], "evidence_ids": ["evidence:001"], "witness_ids": []},
        "revisits": [],
    }

    revised = original.append_relation(relation)
    relation["assertion"]["author"] = "changed-input"
    revised.relations[-1]["provenance"]["evidence_ids"].append("evidence:injected")

    assert [item["id"] for item in original.relations] == ["REL-001", "REL-002"]
    assert revised.relations[-1]["assertion"]["author"] == "another-anonymous"
    assert revised.relations[-1]["provenance"]["evidence_ids"] == ["evidence:001"]


def test_invalid_object_reference_and_promoted_interpretation_are_rejected():
    valid = CulturalTrajectory.from_yaml(FIXTURE)
    unknown_object = deepcopy(valid.document)
    unknown_object["objects"] = [dict(item) for item in valid.document["objects"]]
    unknown_object["relations"] = [dict(item) for item in valid.relations]
    unknown_object["trajectories"] = [dict(item) for item in valid.document["trajectories"]]
    unknown_object["relations"][0]["to"] = "SP-404"
    with pytest.raises(CulturalTrajectoryError, match="unknown object"):
        CulturalTrajectory.from_mapping({"cultural_trajectory": unknown_object})

    promoted = deepcopy(valid.document)
    promoted["objects"] = [dict(item) for item in valid.document["objects"]]
    promoted["relations"] = [dict(item) for item in valid.relations]
    promoted["trajectories"] = [dict(item) for item in valid.document["trajectories"]]
    promoted["relations"][0]["assertion"] = dict(promoted["relations"][0]["assertion"])
    promoted["relations"][0]["assertion"]["verification"] = "verified"
    with pytest.raises(CulturalTrajectoryError, match="must not be promoted"):
        CulturalTrajectory.from_mapping({"cultural_trajectory": promoted})


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda document: document["objects"].append(deepcopy(document["objects"][0])), "duplicate object id"),
        (lambda document: document["relations"].append(deepcopy(document["relations"][0])), "duplicate relation id"),
        (lambda document: document["relations"][0].update({"revisits": ["REL-002"]}), "unknown or future relation"),
        (lambda document: document["trajectories"][0].update({"relation_ids": ["REL-404"]}), "unknown relation"),
    ],
)
def test_invalid_ids_revisits_and_trajectories_are_rejected(mutate, message):
    document = CulturalTrajectory.from_yaml(FIXTURE).document
    mutate(document)

    with pytest.raises(CulturalTrajectoryError, match=message):
        CulturalTrajectory.from_mapping({"cultural_trajectory": document})


def test_oppai_evidence_and_human_gate_stay_separate_from_interpretation():
    trajectory = CulturalTrajectory.from_yaml(FIXTURE)
    observation = normalize("AIが間違えるのって、面白くないか？")
    relation = trajectory.relations[0]
    route = RouteMap.from_mapping("protocol.a", {"protocol.a": ["protocol.b"]})

    assert observation.raw_input == "AIが間違えるのって、面白くないか？"
    assert relation["assertion"]["verification"] == "unverified"
    assert relation["provenance"]["evidence_ids"] == ("evidence:observed-posts-001",) or relation["provenance"]["evidence_ids"] == ["evidence:observed-posts-001"]
    assert route.current == "protocol.a"  # cultural reconstruction does not advance a Runtime route
    decision = process_human_gate(
        candidate=trajectory.human_gate_candidate("REL-001"),
        reviewer_identity="reviewer-1",
        decision="reject",
    )
    assert decision.decision == "reject"
