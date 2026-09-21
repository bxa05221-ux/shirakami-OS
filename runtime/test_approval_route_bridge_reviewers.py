import pytest

from runtime.approval_envelope import ApprovalEnvelope, ApprovalEnvelopeError
from runtime.approval_route_bridge import require_approved_route
from runtime.one_stroke_route_pipeline import RouteSelection


def test_mismatched_reviewer_is_rejected():
    selection = RouteSelection("route-1", ("anmon", "threadrpg"), "human-1")
    envelope = ApprovalEnvelope("route-1", "route-protocol").authorize_execution("human-2")

    with pytest.raises(ApprovalEnvelopeError, match="reviewer"):
        require_approved_route(selection, envelope)


def test_publication_authorization_still_requires_route_execution_approval():
    selection = RouteSelection("route-1", ("anmon", "threadrpg"), "human-1")
    envelope = (
        ApprovalEnvelope("route-1", "route-protocol")
        .authorize_execution("human-1", scope="publication")
        .authorize_publication("human-1")
    )

    assert require_approved_route(selection, envelope) == selection
