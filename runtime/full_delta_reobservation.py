"""Full replay versus checkpoint-plus-delta re-observation boundary."""

from collections.abc import Iterable, Mapping

from .adapter import Adapter, adapt_landscape_observation
from .delta_reobservation import execute_and_reobserve
from .evidence import EvidenceRecord
from .evidence_replay import replay_evidence


def compare_full_and_delta_reobservation(
    snapshot: Mapping,
    evidence: Iterable[EvidenceRecord],
    applied: Iterable[EvidenceRecord],
    adapter: Adapter,
):
    """Compare snapshot equivalence while preserving lineage differences."""
    records = list(evidence)
    full_state = replay_evidence(records)
    full_observation = adapt_landscape_observation(full_state)
    delta_result = execute_and_reobserve(snapshot, records, applied, adapter)
    delta_observation = delta_result["observation"]
    return {
        "full": full_observation,
        "delta": delta_observation,
        "snapshot_equivalent": full_observation["snapshot"] == delta_observation["snapshot"],
        "lineage_equivalent": full_observation["evidence_lineage"] == delta_observation["evidence_lineage"],
    }
