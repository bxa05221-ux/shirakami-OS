"""Historical Protocol-version selection during deterministic Evidence replay."""

from collections.abc import Iterable, Mapping

from .evidence import EvidenceRecord
from .landscape import LandscapeState


def protocol_version_from_evidence(evidence: EvidenceRecord) -> str | None:
    """Read the historical Protocol version carried by an observed transition."""
    value = evidence.transition_data.get("protocol_version")
    return str(value) if value is not None else None


def replay_with_historical_protocol_versions(
    evidence: Iterable[EvidenceRecord],
    current_versions: Mapping[str, str],
) -> dict:
    """Replay Evidence while preserving historical Protocol-version references."""
    records = list(evidence)
    state = LandscapeState.empty()
    lineage = []

    for record in records:
        historical_version = protocol_version_from_evidence(record)
        current_version = current_versions.get(record.protocol_id)
        lineage.append(
            {
                "protocol_id": record.protocol_id,
                "historical_version": historical_version,
                "current_version": current_version,
            }
        )
        state.apply_evidence(record)

    return {"snapshot": state.snapshot(), "protocol_version_lineage": tuple(lineage)}
