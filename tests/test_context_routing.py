from runtime.context_routing import context_lineage, route_context


def test_context_routing_is_request_scoped():
    handoff = {
        "evidence_ids": ["e-001", "e-002"],
        "protocol_ids": ["p-001"],
        "runtime_ids": ["r-001"],
        "irrelevant_memory": ["must-not-be-recalled"],
    }

    selection = route_context(handoff, request_id="req-001")

    assert selection.request_id == "req-001"
    assert selection.evidence_ids == ("e-001", "e-002")
    assert selection.protocol_ids == ("p-001",)
    assert selection.runtime_ids == ("r-001",)
    assert "irrelevant_memory" not in context_lineage(selection)


def test_context_routing_does_not_invent_missing_context():
    selection = route_context({}, request_id="req-002")

    assert selection.evidence_ids == ()
    assert selection.protocol_ids == ()
    assert selection.runtime_ids == ()
