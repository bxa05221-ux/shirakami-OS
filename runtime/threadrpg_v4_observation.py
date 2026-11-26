"""Non-authoritative ThreadRPG v4 observation -> Evidence adapter.

Records provenance without asserting user facts, invoking LLMs, or applying
Landscape transitions. Raw thread history stays in AATS Thread.
"""
from dataclasses import dataclass
from typing import Literal

from runtime.aats import Thread
from runtime.evidence import EvidenceRecord
from runtime.evidence_store import EvidenceStore

Origin = Literal["human_post", "anonymous_generated", "hypothesis", "joke", "unknown"]


@dataclass(frozen=True)
class Observation:
    post_index: int
    origin: Origin
    text: str
    preceding_refs: tuple[int, ...] = ()


def observe_post(thread: Thread, post_index: int, *, origin: Origin,
                 preceding_refs: tuple[int, ...] = ()) -> Observation:
    """Explicit classification; never infer a joke or hypothesis as fact."""
    if not 0 <= post_index < len(thread.posts):
        raise IndexError("post index out of range")
    post = thread.posts[post_index]
    if origin == "human_post" and post.participant_id != "icchi":
        raise ValueError("only Icchi posts can be human_post")
    if origin != "human_post" and post.participant_id == "icchi":
        raise ValueError("Icchi posts cannot be reclassified as generated")
    if any(not 0 <= ref < post_index for ref in preceding_refs):
        raise ValueError("preceding refs must point to earlier posts")
    return Observation(post_index, origin, post.text, preceding_refs)


def record_observation(thread: Thread, observation: Observation,
                       store: EvidenceStore) -> EvidenceStore:
    """Append observational Evidence only; no transition_data.changed."""
    if not isinstance(store, EvidenceStore):
        raise TypeError("store must be EvidenceStore")
    if not 0 <= observation.post_index < len(thread.posts):
        raise ValueError("observation refers to absent post")
    post = thread.posts[observation.post_index]
    if post.text != observation.text:
        raise ValueError("observation text differs from raw log")
    if (observation.origin == "human_post") != (post.participant_id == "icchi"):
        raise ValueError("observation origin differs from raw log")
    if any(not 0 <= ref < observation.post_index for ref in observation.preceding_refs):
        raise ValueError("invalid preceding reference")
    record = EvidenceRecord(
        protocol_id="threadrpg.v4.observation",
        status="observed",
        transition_kind="observation",
        transition_data={
            "thread_id": thread.thread_id,
            "post_index": observation.post_index,
            "origin": observation.origin,
            "text": observation.text,
            "preceding_refs": list(observation.preceding_refs),
        },
        signals=("non_authoritative", observation.origin),
        confidence="unverified",
    )
    return store.append(record)
