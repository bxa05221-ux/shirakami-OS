"""Request-scoped Context Routing for Shirakami Runtime v0.1.

Context Routing selects explicitly requested context references instead of
replaying the entire conversation or model memory. It does not interpret,
rank, or infer authority from the selected records.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class ContextSelection:
    """Explicit references selected for one request."""

    request_id: str
    evidence_ids: tuple[str, ...] = ()
    protocol_ids: tuple[str, ...] = ()
    runtime_ids: tuple[str, ...] = ()


def route_context(
    handoff: Mapping[str, Any],
    *,
    request_id: str,
) -> ContextSelection:
    """Route only explicitly declared context references for a request.

    Missing reference lists remain empty. The router never searches the whole
    conversation, invents references, or converts model interpretation into
    authority.
    """
    return ContextSelection(
        request_id=request_id,
        evidence_ids=tuple(str(x) for x in handoff.get("evidence_ids", ())),
        protocol_ids=tuple(str(x) for x in handoff.get("protocol_ids", ())),
        runtime_ids=tuple(str(x) for x in handoff.get("runtime_ids", ())),
    )


def context_lineage(selection: ContextSelection) -> dict[str, Any]:
    """Return JSON-ready lineage for the selected request-scoped context."""
    return {
        "request_id": selection.request_id,
        "evidence_ids": list(selection.evidence_ids),
        "protocol_ids": list(selection.protocol_ids),
        "runtime_ids": list(selection.runtime_ids),
    }
