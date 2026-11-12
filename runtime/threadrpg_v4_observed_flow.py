"""Explicit ThreadRPG v4 flow with append-only observation Evidence."""
from dataclasses import dataclass

from runtime.aats import Thread
from runtime.evidence_store import EvidenceStore
from runtime.threadrpg_v4_evidence_bridge import capture_threadrpg_observation
from runtime.threadrpg_v4_minimal_flow import (
    MinimalFlowResult,
    ReplyGenerator,
    run_minimal_flow,
)


@dataclass(frozen=True)
class ObservedFlowResult:
    flow: MinimalFlowResult
    store: EvidenceStore


def run_observed_flow(
    thread: Thread,
    raw_input: str | None,
    generator: ReplyGenerator,
    store: EvidenceStore,
) -> ObservedFlowResult:
    if not isinstance(store, EvidenceStore):
        raise TypeError("store must be EvidenceStore")

    flow = run_minimal_flow(thread, raw_input, generator)
    evidence = capture_threadrpg_observation(flow)
    return ObservedFlowResult(flow, store.append(evidence))
