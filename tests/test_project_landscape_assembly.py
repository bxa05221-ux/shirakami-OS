from runtime.project_landscape_assembly import assemble_landscape
from runtime.project_landscape_loader import LoadedSource
from runtime.source_registry import SourceRef


def test_assembly_preserves_source_boundaries_and_metadata():
    ref = SourceRef(
        id="design.example",
        type="design",
        path="design/example.yaml",
        status="active",
        authority="primary",
        version="0.1",
    )
    content = {"opaque": "value"}
    landscape = assemble_landscape(
        [LoadedSource(ref=ref, content=content)],
        ["question remains open"],
    )

    assert landscape.sources[0].source.ref == ref
    assert landscape.sources[0].source.content is content
    assert landscape.unresolved_questions == ("question remains open",)


def test_assembly_does_not_merge_source_content():
    ref_a = SourceRef("a", "design", "a.yaml", "active", "primary")
    ref_b = SourceRef("b", "implementation", "b.py", "implemented", "primary")
    content_a = {"a": 1}
    content_b = {"b": 2}

    landscape = assemble_landscape(
        [
            LoadedSource(ref_a, content_a),
            LoadedSource(ref_b, content_b),
        ]
    )

    assert [item.source.ref.id for item in landscape.sources] == ["a", "b"]
    assert landscape.sources[0].source.content is content_a
    assert landscape.sources[1].source.content is content_b
