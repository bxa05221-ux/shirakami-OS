"""Request-scoped Context Bundle for Shirakami Runtime v0.1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from runtime.context_routing import ContextSelection
from runtime.evidence_resolver import ResolvedEvidence


@dataclass(frozen=True)
class ContextBundle:
    """Concrete context admitted to one Runtime request."""

    request_id: str
    evidence: tuple[ResolvedEvidence, ...] = ()
    protocol_ids: tuple[str, ...] = ()
    runtime_ids: tuple[str, ...] = ()

    @classmethod
    def from_selection(
        cls,
        selection: ContextSelection,
        evidence: Sequence[ResolvedEvidence],
    ) -> "ContextBundle":
        """Build a bundle without adding context beyond the selection."""
        if any(item.request_id != selection.request_id for item in evidence):
            raise ValueError("Evidence request_id does not match selection")

        resolved_ids = tuple(item.evidence_id for item in evidence)
        if resolved_ids != selection.evidence_ids:
            raise ValueError("Resolved Evidence does not match selection")

        return cls(
            request_id=selection.request_id,
            evidence=tuple(evidence),
            protocol_ids=selection.protocol_ids,
            runtime_ids=selection.runtime_ids,
        )


def bundle_lineage(bundle: ContextBundle) -> dict[str, Any]:
    """Return the auditable context boundary for a Runtime request."""
    return {
        "request_id": bundle.request_id,
        "evidence_ids": [item.evidence_id for item in bundle.evidence],
        "protocol_ids": list(bundle.protocol_ids),
        "runtime_ids": list(bundle.runtime_ids),
    }


def bundle_payload(bundle: ContextBundle) -> Mapping[str, Any]:
    """Return JSON-ready payload containing only admitted context."""
    return {
        "request_id": bundle.request_id,
        "evidence": [
            {
                "evidence_id": item.evidence_id,
                "record": dict(item.record),
            }
            for item in bundle.evidence
        ],
        "protocol_ids": list(bundle.protocol_ids),
        "runtime_ids": list(bundle.runtime_ids),
    }
