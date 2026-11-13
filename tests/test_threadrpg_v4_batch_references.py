import pytest

from runtime.aats import Thread
from runtime.threadrpg_v4_minimal_flow import (
    AnonymousReply, ReplyProposal, run_minimal_flow
)


def test_anonymous_reply_can_reference_earlier_batch_reply():
    def generator(thread, event):
        return ReplyProposal((
            AnonymousReply("first", (0,)),
            AnonymousReply(">>2 second", batch_reply_indices=(0,)),
            AnonymousReply(">>3 third", batch_reply_indices=(1,)),
        ))

    result = run_minimal_flow(Thread("batch-reference"), "question", generator)

    assert len(result.thread.posts) == 4
    assert result.resolved_reply_references == (
        (0,),
        (1,),
        (2,),
    )
    assert result.human_gate_required is True
    assert result.reality_mutation_permitted is False


@pytest.mark.parametrize("invalid_reference", [
    (0,),
    (1,),
    (-1,),
    (99,),
])
def test_batch_reference_cannot_point_forward_or_to_itself(invalid_reference):
    def generator(thread, event):
        return ReplyProposal((
            AnonymousReply("first", batch_reply_indices=invalid_reference),
            AnonymousReply("second"),
        ))

    with pytest.raises(ValueError, match="batch references"):
        run_minimal_flow(Thread("invalid-batch"), "question", generator)


def test_existing_reference_behavior_is_preserved():
    def generator(thread, event):
        return ReplyProposal((
            AnonymousReply("first", (0,)),
            AnonymousReply("second"),
        ))

    result = run_minimal_flow(Thread("legacy-reference"), "question", generator)

    assert result.resolved_reply_references == ((0,), ())
