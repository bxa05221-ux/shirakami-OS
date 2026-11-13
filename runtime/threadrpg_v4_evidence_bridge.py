"""Observation-only Evidence bridge for ThreadRPG v4.

Generated posts are observations, not verified facts or authorization.
No persistence, network calls, or Reality mutation.
"""
from runtime.evidence import EvidenceRecord
from runtime.threadrpg_v4_minimal_flow import MinimalFlowResult


def capture_threadrpg_observation(result: MinimalFlowResult) -> EvidenceRecord:
    if not isinstance(result, MinimalFlowResult):
        raise TypeError("expected MinimalFlowResult")
    if result.reality_mutation_permitted:
        raise ValueError("Reality mutation must remain prohibited")
    if not result.human_gate_required:
        raise ValueError("Human Gate must remain required")

    return EvidenceRecord(
        protocol_id="threadrpg.v4",
        status="observed",
        transition_kind="threadrpg.v4.reply_batch.observed",
        transition_data={
            "thread_id": result.thread.thread_id,
            "event_kind": result.event.kind,
            "post_count": len(result.thread.posts),
            "replies": [
                {
                    "text": reply.text,
                    "source_post_indices": list(reply.source_post_indices),
                    "batch_reply_indices": list(reply.batch_reply_indices),
                    "resolved_post_indices": list(resolved),
                }
                for reply, resolved in zip(
                    result.replies, result.resolved_reply_references
                )
            ],
            "human_gate_required": True,
            "reality_mutation_permitted": False,
        },
        signals=("THREADRPG_GENERATED_OUTPUT_OBSERVED",),
        confidence="observed",
    )
