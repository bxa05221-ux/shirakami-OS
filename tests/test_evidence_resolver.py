import pytest

from runtime.evidence_resolver import (
    EvidenceResolutionError,
    evidence_lineage,
    resolve_evidence,
)


def test_resolver_preserves_explicit_order_and_scope():
    store = {
        "e-001": {"value": "first"},
        "e-002": {"value": "second"},
        "e-003": {"value": "not-requested"},
    }

    resolved = resolve_evidence(
        ("e-002", "e-001"),
        store,
        request_id="req-001",
    )

    assert [item.evidence_id for item in resolved] == ["e-002", "e-001"]
    assert [item.record["value"] for item in resolved] == ["second", "first"]
    assert evidence_lineage(resolved) == {
        "request_id": "req-001",
        "evidence_ids": ["e-002", "e-001"],
    }


def test_resolver_does_not_silently_omit_missing_evidence():
    with pytest.raises(EvidenceResolutionError, match="e-404"):
        resolve_evidence(
            ("e-001", "e-404"),
            {"e-001": {"value": "known"}},
            request_id="req-002",
        )


def test_resolver_does_not_invent_records_for_empty_selection():
    resolved = resolve_evidence(
        (),
        {"e-001": {"value": "known"}},
        request_id="req-003",
    )

    assert resolved == ()
    assert evidence_lineage(resolved) == {
        "request_id": None,
        "evidence_ids": [],
    }
