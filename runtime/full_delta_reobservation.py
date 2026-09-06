"""Full replay versus checkpoint-plus-delta re-observation boundary."""

from collections.abc import Iterable, Mapping

from .adapter import Adapter
from .delta_reobservation import execute_and_reobserve
from .evidence import EvidenceRecord
from .evidence_replay import replay_evidence


def compare_full_and_delta_reobservation(
    snapshot: Mapping,
    evidence: Iterable[EvidenceRecord],
    applied: Iterable[EvidenceRecord],
    adapter: Adapter,
):
    """Compare observable results of full replay and checkpoint-plus-delta execution."""
    records = list(evidence)
    full_state = replay_evidence(records)
    full_observation = adapter.adapt_landscape_observation(full_state)
    delta_result = execute_and_reobserve(snapshot, records, applied, adapter)
    return {
        "full": full_observation,
        "delta": delta_result["observation"],
        "equivalent": full_observation == delta_result["observation"],
    }
