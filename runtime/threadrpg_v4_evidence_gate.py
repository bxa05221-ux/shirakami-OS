"""Evidence lookup boundary for ThreadRPG v4.

Evidence existence is not human approval.
"""
from runtime.evidence_store import EvidenceStore
from runtime.aats import Thread


def observation_evidence_matches(
    store: EvidenceStore,
    thread: Thread,
    post_index: int,
    evidence_id: str,
) -> bool:
    if not isinstance(store, EvidenceStore):
        return False
    if not isinstance(thread, Thread):
        return False
    if not isinstance(post_index, int) or isinstance(post_index, bool):
        return False
    if not 0 <= post_index < len(thread.posts):
        return False
    if not isinstance(evidence_id, str) or not evidence_id:
        return False

    post = thread.posts[post_index]

    for record in store.all():
        if record.evidence_id != evidence_id:
            continue
        if record.protocol_id != "threadrpg.v4.observation":
            continue
        if record.status != "observed":
            continue
        if record.transition_kind != "observation":
            continue
        if record.confidence != "unverified":
            continue

        data = record.transition_data
        return (
            data.get("thread_id") == thread.thread_id
            and data.get("post_index") == post_index
            and data.get("text") == post.text
            and (
                (data.get("origin") == "human_post")
                == (post.participant_id == "icchi")
            )
        )

    return False
