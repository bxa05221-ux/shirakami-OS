"""Regression tests for the read-only Cultural Trajectory review projection."""
import json

from runtime.aats import Participant, Post, Thread
from runtime.cultural_trajectory_review import cultural_trajectory_review
from runtime.threadrpg_cultural_trajectory import observe_threadrpg_thread


def _thread():
    return (
        Thread("synthetic-review-001")
        .with_participant(Participant("anonymous-1"))
        .with_participant(Participant("anonymous-2"))
        .with_post(Post("anonymous-1", "AIが間違えるのって、面白くないか？"))
        .with_post(Post("anonymous-2", "間違いを信じたら危ない。"))
    )


def test_review_is_json_serializable_and_keeps_source_order():
    thread = _thread()
    before = thread.snapshot()
    turn = observe_threadrpg_thread(thread)
    review = cultural_trajectory_review(turn)

    assert json.loads(json.dumps(review)) == review
    assert [post["original_text"] for post in review["posts"]] == [
        post["text"] for post in before["posts"]
    ]
    assert [post["spark_id"] for post in review["posts"]] == ["SP-001", "SP-002"]
    assert review["status"] == "candidate_only"
    assert review["evidence_resolution"] == "not_implemented"
    assert review["verification"] == "unverified"
    assert review["relations"][0]["assertion"]["verification"] == "unverified"
    assert review["relations"][0]["provenance"]["evidence_ids"] == [
        "evidence:synthetic-review-001"
    ]
    assert thread.snapshot() == before


def test_review_is_detached_and_revisit_preserves_original_history():
    thread = _thread()
    turn = observe_threadrpg_thread(thread)
    before = thread.snapshot()
    original = cultural_trajectory_review(turn)
    original["posts"][0]["original_text"] = "modified"
    original["relations"][0]["assertion"]["verification"] = "verified"
    original["trajectories"][0]["relation_ids"].clear()

    fresh = cultural_trajectory_review(turn)
    assert fresh["posts"][0]["original_text"] == before["posts"][0]["text"]
    assert fresh["relations"][0]["assertion"]["verification"] == "unverified"
    assert fresh["trajectories"][0]["relation_ids"] == ["REL-001"]

    turn.revisit("contradicts")
    revisited = cultural_trajectory_review(turn)
    assert len(revisited["relations"]) == 2
    assert revisited["relations"][0] == fresh["relations"][0]
    assert revisited["revisit_relations"][0]["revisits"] == ["REL-001"]
    assert revisited["revisit_relations"][0]["assertion"]["verification"] == "unverified"
    assert thread.snapshot() == before
