from runtime.aats import Thread
from runtime.evidence_store import EvidenceStore
from runtime.threadrpg_v4_evidence_bridge import capture_threadrpg_observation
from runtime.threadrpg_v4_minimal_flow import (
    AnonymousReply,
    ReplyProposal,
    run_minimal_flow,
)


def test_threadrpg_observation_preserves_provenance():
    def generator(thread, event):
        return ReplyProposal((
            AnonymousReply("それな", source_post_indices=(0,)),
            AnonymousReply(">>2 いや違う", batch_reply_indices=(0,)),
        ))

    result = run_minimal_flow(Thread("vip-evidence"), "議論しよう", generator)
    record = capture_threadrpg_observation(result)

    assert record.protocol_id == "threadrpg.v4"
    assert record.status == "observed"
    assert record.transition_data["replies"][0]["resolved_post_indices"] == [0]
    assert record.transition_data["replies"][1]["resolved_post_indices"] == [1]
    assert record.transition_data["reality_mutation_permitted"] is False
    assert record.transition_data["human_gate_required"] is True

    store = EvidenceStore().append(record)
    assert store.by_protocol("threadrpg.v4") == (record,)


def test_invalid_generation_does_not_produce_evidence():
    def invalid_generator(thread, event):
        return ReplyProposal(())

    original = Thread("vip-invalid")
    store = EvidenceStore()

    try:
        run_minimal_flow(original, "テスト", invalid_generator)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid generation was accepted")

    assert original.posts == ()
    assert store.all() == ()
