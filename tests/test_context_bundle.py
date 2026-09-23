from runtime.context_bundle import bundle_lineage, bundle_payload
from runtime.context_routing import route_context
from runtime.evidence_resolver import resolve_evidence


def test_context_bundle_contains_only_routed_and_resolved_context():
    selection = route_context(
        {
            "evidence_ids": ["e-002", "e-001"],
            "protocol_ids": ["p-001"],
            "runtime_ids": ["r-001"],
            "unrelated": ["must-not-enter"],
        },
        request_id="req-001",
    )
    resolved = resolve_evidence(
        selection.evidence_ids,
        {
            "e-001": {"value": "first"},
            "e-002": {"value": "second"},
            "e-999": {"value": "unrequested"},
        },
        request_id="req-001",
    )

    from runtime.context_bundle import ContextBundle
    bundle = ContextBundle.from_selection(selection, resolved)

    assert bundle_lineage(bundle) == {
        "request_id": "req-001",
        "evidence_ids": ["e-002", "e-001"],
        "protocol_ids": ["p-001"],
        "runtime_ids": ["r-001"],
    }
    assert bundle_payload(bundle) == {
        "request_id": "req-001",
        "evidence": [
            {"evidence_id": "e-002", "record": {"value": "second"}},
            {"evidence_id": "e-001", "record": {"value": "first"}},
        ],
        "protocol_ids": ["p-001"],
        "runtime_ids": ["r-001"],
    }


def test_context_bundle_rejects_wrong_request_lineage():
    selection = route_context(
        {"evidence_ids": ["e-001"]},
        request_id="req-001",
    )
    resolved = resolve_evidence(
        ("e-001",),
        {"e-001": {"value": "known"}},
        request_id="req-002",
    )

    from runtime.context_bundle import ContextBundle
    try:
        ContextBundle.from_selection(selection, resolved)
    except ValueError as exc:
        assert "request_id" in str(exc)
    else:
        raise AssertionError("mismatched request lineage must be rejected")
