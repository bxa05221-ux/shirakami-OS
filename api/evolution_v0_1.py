"""Minimal HTTP-facing Evolution Loop v0.1 adapter.

This module keeps the API boundary thin while admitting only request-scoped
context selected by Context Routing and resolved by Evidence Resolver.
"""

from __future__ import annotations

from typing import Any, Mapping

from runtime.backend import Backend
from runtime.context_bundle import ContextBundle, bundle_payload
from runtime.context_routing import route_context
from runtime.evidence_resolver import resolve_evidence
from runtime.evolution_loop import execute_and_observe


def _admit_context(handoff: Mapping[str, Any]) -> Mapping[str, Any]:
    """Build an explicit Context Bundle when context references are supplied."""
    if "evidence_ids" not in handoff:
        return handoff

    request_id = str(handoff.get("request_id", handoff.get("handoff_id", "")))
    selection = route_context(handoff, request_id=request_id)
    store = handoff.get("evidence_store", {})
    if not isinstance(store, Mapping):
        raise TypeError("evidence_store must be a mapping")

    resolved = resolve_evidence(
        selection.evidence_ids,
        store,
        request_id=request_id,
    )
    bundle = ContextBundle.from_selection(selection, resolved)

    admitted = dict(handoff)
    admitted["context_bundle"] = bundle_payload(bundle)
    admitted["context_lineage"] = bundle_payload(bundle)["request_id"]
    admitted.pop("evidence_store", None)
    return admitted


def execute_evolution_v0_1(
    backend: Backend,
    handoff: Mapping[str, Any],
) -> dict[str, Any]:
    """Execute an authorized handoff with optional explicit context admission."""
    admitted_handoff = _admit_context(handoff)
    evidence = execute_and_observe(backend, admitted_handoff)
    return {
        "evidence_id": evidence.evidence_id,
        "protocol_id": evidence.protocol_id,
        "status": evidence.status,
        "transition_kind": evidence.transition_kind,
        "transition_data": dict(evidence.transition_data),
        "signals": list(evidence.signals),
        "confidence": evidence.confidence,
    }
