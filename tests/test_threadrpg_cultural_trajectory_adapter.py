"""Synthetic ThreadRPG-turn coverage for the Cultural Trajectory PoC.

This fixture deliberately contains no user log: it represents a small,
anonymous ThreadRPG-like exchange solely for the adapter boundary test.
"""

from runtime.threadrpg_cultural_trajectory import observe_threadrpg_turn


SYNTHETIC_THREAD_LOG = (
    {
        "id": "synthetic-thread-001:post-001",
        "speaker": "anonymous-1",
        "text": "AIが間違えるのって、面白くないか？",
    },
    {
        "id": "synthetic-thread-001:post-002",
        "speaker": "anonymous-2",
        "text": "間違いをそのまま信じたら危ない。",
    },
)


def test_synthetic_threadrpg_turn_preserves_source_and_connects_candidates_to_revisit():
    result = observe_threadrpg_turn(SYNTHETIC_THREAD_LOG)

    assert [item["text"] for item in result.sparks] == [item["text"] for item in SYNTHETIC_THREAD_LOG]
    assert result.sparks[0]["source_ref"] == "synthetic-thread-001:post-001"
    assert result.oppai_observations[1].raw_input == SYNTHETIC_THREAD_LOG[1]["text"]

    relation = result.relation_candidate
    assert relation["assertion"]["verification"] == "unverified"
    assert relation["provenance"]["evidence_ids"] == ["evidence:synthetic-thread-001"]
    assert result.trajectory.reconstruct("TRJ-synthetic-thread-001") == (relation,)

    revisited = result.revisit("resonates")
    assert revisited["revisits"] == [relation["id"]]
    assert revisited["assertion"]["verification"] == "unverified"
    assert [item["id"] for item in result.trajectory.relations] == [relation["id"]]
    assert [item["id"] for item in result.revisited_trajectory.relations] == [relation["id"], revisited["id"]]
