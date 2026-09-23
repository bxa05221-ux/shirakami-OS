"""Explicit Evidence resolution for Shirakami Runtime v0.1.

Evidence Resolver resolves only IDs selected by Context Routing. It does not
search, rank, infer, or silently omit requested records.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


class EvidenceResolutionError(KeyError):
    """Raised when an explicitly requested Evidence ID cannot be resolved."""


@dataclass(frozen=True)
class ResolvedEvidence:
    """One resolved Evidence record with request-scoped lineage."""

    request_id: str
    evidence_id: str
    record: Mapping[str, Any]


def resolve_evidence(
    evidence_ids: Sequence[str],
    store: Mapping[str, Mapping[str, Any]],
    *,
    request_id: str,
) -> tuple[ResolvedEvidence, ...]:
    """Resolve explicit Evidence IDs in the caller's declared order.

    The resolver never performs semantic retrieval or adds unrequested
    records. A missing requested ID is an explicit resolution failure.
    """
    resolved: list[ResolvedEvidence] = []
    for evidence_id in evidence_ids:
        key = str(evidence_id)
        if key not in store:
            raise EvidenceResolutionError(
                f"Evidence record not found: {key}"
            )
        resolved.append(
            ResolvedEvidence(
                request_id=request_id,
                evidence_id=key,
                record=store[key],
            )
        )
    return tuple(resolved)


def evidence_lineage(
    resolved: Sequence[ResolvedEvidence],
) -> dict[str, Any]:
    """Return JSON-ready lineage without changing the Evidence records."""
    return {
        "request_id": resolved[0].request_id if resolved else None,
        "evidence_ids": [item.evidence_id for item in resolved],
    }
