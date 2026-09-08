from runtime.context_boundary import create_context_snapshot
from runtime.project_landscape_assembly import ProjectLandscape, LandscapeSource
from runtime.project_landscape_loader import LoadedSource
from runtime.source_registry import SourceRef


def source(source_id: str) -> LandscapeSource:
    ref = SourceRef(source_id, "design", f"{source_id}.yaml", "active", "primary")
    return LandscapeSource(LoadedSource(ref, {source_id: "opaque"}))


def test_context_is_a_scoped_view_and_preserves_questions():
    landscape = ProjectLandscape(
        sources=(source("a"), source("b")),
        unresolved_questions=("still unknown",),
    )

    context = create_context_snapshot(
        landscape,
        context_id="ctx-1",
        parent_landscape_ref="landscape-1",
        requested_context="writer",
        source_ids=["b"],
    )

    assert context.context_id == "ctx-1"
    assert context.parent_landscape_ref == "landscape-1"
    assert [item.source.ref.id for item in context.source_refs] == ["b"]
    assert context.unresolved_questions == ("still unknown",)
    assert context.requested_context == "writer"


def test_context_does_not_replace_landscape():
    landscape = ProjectLandscape(sources=(source("a"), source("b")))
    context = create_context_snapshot(
        landscape,
        context_id="ctx-2",
        parent_landscape_ref="landscape-2",
    )

    assert len(context.source_refs) == len(landscape.sources)
    assert context.source_refs[0].source.content is landscape.sources[0].source.content
