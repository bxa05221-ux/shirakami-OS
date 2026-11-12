import pytest

from runtime.aats import Thread
from runtime.evidence_store import EvidenceStore
from runtime.threadrpg_v4_minimal_flow import AnonymousReply, ReplyProposal
from runtime.threadrpg_v4_observed_flow import run_observed_flow


def test_observed_flow_appends_evidence():
    def generator(thread, event):
        return ReplyProposal((
            AnonymousReply("それな", source_post_indices=(0,)),
        ))

    original = Thread("vip-observed")
    initial_store = EvidenceStore()

    result = run_observed_flow(
        original, "イッチの投稿", generator, initial_store
    )

    assert len(result.flow.thread.posts) == 2
    assert original.posts == ()
    assert initial_store.all() == ()

    records = result.store.by_protocol("threadrpg.v4")
    assert len(records) == 1
    assert records[0].transition_data["replies"][0]["text"] == "それな"
    assert records[0].status == "observed"


def test_invalid_flow_preserves_original_store():
    def generator(thread, event):
        return ReplyProposal(())

    original = Thread("vip-failed")
    initial_store = EvidenceStore()

    with pytest.raises(ValueError):
        run_observed_flow(original, "投稿", generator, initial_store)

    assert original.posts == ()
    assert initial_store.all() == ()
