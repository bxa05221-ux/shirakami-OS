"""Explicit bridge between Human Gate route selection and approval metadata.

This module validates an already-selected route against an explicit
ApprovalEnvelope. It does not select routes, invoke Protocols, or authorize
anything implicitly.
"""
from __future__ import annotations

try:
    from .approval_envelope import ApprovalEnvelope, ApprovalEnvelopeError
    from .one_stroke_route_pipeline import RouteSelection
except ImportError:
    from approval_envelope import ApprovalEnvelope, ApprovalEnvelopeError
    from one_stroke_route_pipeline import RouteSelection


def require_approved_route(
    selection: RouteSelection,
    envelope: ApprovalEnvelope,
) -> RouteSelection:
    """Return the route only when the envelope explicitly authorizes execution."""
    if envelope.candidate_id != selection.route_id:
        raise ApprovalEnvelopeError("envelope candidate does not match route selection")
    if envelope.reviewer != selection.reviewer:
        raise ApprovalEnvelopeError("envelope reviewer does not match route reviewer")
    if not envelope.execution_authorized:
        raise ApprovalEnvelopeError("route execution requires explicit approval")
    return selection
