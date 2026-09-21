import pytest

from runtime.approval_envelope import ApprovalEnvelope, ApprovalEnvelopeError
from runtime.approval_route_bridge import require_approved_route
from runtime.one_stroke_route_pipeline import RouteSelection


def test_unapproved_envelope_cannot_cross_route_boundary():
    selection = RouteSelection("route-1", ("anmon", "threadrpg"), "human-1")
    envelope = ApprovalEnvelope("route-1", "route-protocol")

    with pytest.raises(ApprovalEnvelopeError):
        require_approved_route(selection, envelope)


def test_approved_envelope_must_match_route_and_reviewer():
    selection = RouteSelection("route-1", ("anmon", "threadrpg"), "human-1")
    envelope = ApprovalEnvelope("route-1", "route-protocol").authorize_execution("human-1")

    assert require_approved_route(selection, envelope) == selection


def test_mismatched_candidate_is_rejected():
    selection = RouteSelection("route-1", ("anmon", "threadrpg"), "human-1")
    envelope = ApprovalEnvelope("route-2", "route-protocol").authorize_execution("human-1")

    with pytest.raises(ApprovalEnvelopeError):
        require_approved_route(selection, envelope)
