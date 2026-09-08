from runtime.project_landscape_loader import load_landscape
from runtime.source_registry import SourceRef


def ref(source_id, source_type="design", status="active"):
    return SourceRef(source_id, source_type, f"{source_id}.yaml", status, "primary")


def test_loader_preserves_registry_order_and_content():
    refs = (ref("matome", "matome_yaml"), ref("design"), ref("implementation", "implementation"))
    result = load_landscape(refs, {"matome": {"x": 1}, "design": "design-content", "implementation": "code-ref"})
    assert [item.ref.id for item in result.sources] == ["matome", "design", "implementation"]
    assert result.sources[0].content == {"x": 1}
    assert result.unresolved_questions == ()


def test_loader_does_not_fabricate_missing_content():
    refs = (ref("design"), ref("missing"))
    result = load_landscape(refs, {"design": "content"})
    assert [item.ref.id for item in result.sources] == ["design"]
    assert result.unresolved_questions == ("source content unavailable: missing",)


def test_loader_skips_non_active_sources_by_default():
    refs = (ref("active"), ref("archived", status="archived"))
    result = load_landscape(refs, {"active": "a", "archived": "old"})
    assert [item.ref.id for item in result.sources] == ["active"]
