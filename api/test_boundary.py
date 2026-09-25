import pytest

from api.boundary import validate_execution_context


def _context():
    return {
        "handoff_id": "SH-HO-20260925-001",
        "project": "Shirakami Project",
        "objective": "Validate the API boundary",
        "protocol_ids": ["Local Repository Operation Protocol v0.1"],
        "evidence_ids": ["AGENT-COORDINATION-001"],
        "verification_scope": ["API boundary"],
    }


def test_execution_context_is_admissible_without_authority():
    result = validate_execution_context(_context())
    assert result["handoff_id"] == "SH-HO-20260925-001"
    assert result["evidence_ids"] == ["AGENT-COORDINATION-001"]
    assert result["execution_authorized"] is False
    assert result["publish_authorized"] is False
    assert result["merge_authorized"] is False
    assert result["human_gate_required"] is True


@pytest.mark.parametrize(
    "field",
    ["handoff_id", "project", "objective", "protocol_ids", "evidence_ids", "verification_scope"],
)
def test_missing_required_boundary_field_is_rejected(field):
    context = _context()
    del context[field]
    with pytest.raises(ValueError, match="missing required boundary fields"):
        validate_execution_context(context)


@pytest.mark.parametrize(
    "field",
    ["execution_authorized", "publish_authorized", "merge_authorized"],
)
def test_authority_cannot_cross_boundary(field):
    context = _context()
    context[field] = True
    with pytest.raises(ValueError, match=field):
        validate_execution_context(context)


def test_human_gate_cannot_be_disabled():
    context = _context()
    context["human_gate_required"] = False
    with pytest.raises(ValueError, match="human_gate_required"):
        validate_execution_context(context)
