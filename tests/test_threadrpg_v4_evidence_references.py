from runtime.aats import Thread
from runtime.evidence_store import EvidenceStore
from runtime.threadrpg_v4_minimal_flow import (
    AnonymousReply, ReplyProposal, run_minimal_flow
)
from runtime.threadrpg_v4_observation import observe_post, record_observation


def test_batch_references_are_preserved_in_evidence():
    def generator(thread, event):
        return ReplyProposal((
            AnonymousReply("first", (0,)),
            AnonymousReply(">>2 second", batch_reply_indices=(0,)),
            AnonymousReply(">>3 third", batch_reply_indices=(1,)),
        ))

    result = run_minimal_flow(Thread("evidence-refs"), "question", generator)
    store = EvidenceStore()

    for index, post in enumerate(result.thread.posts):
        if post.participant_id == "icchi":
            refs = ()
            origin = "human_post"
        else:
            reply_index = index - 1
            refs = result.resolved_reply_references[reply_index]
            origin = "anonymous_generated"

        observation = observe_post(
            result.thread,
            index,
            origin=origin,
            preceding_refs=refs,
        )
        store = record_observation(result.thread, observation, store)

    records = store.all()
    assert len(records) == 4
    assert records[1].transition_data["preceding_refs"] == [0]
    assert records[2].transition_data["preceding_refs"] == [1]
    assert records[3].transition_data["preceding_refs"] == [2]

    for record in records[1:]:
        assert record.confidence == "unverified"
        assert "non_authoritative" in record.signals
        assert record.transition_data.get("changed") is not True
