import pytest

from runtime.context_boundary import create_context_snapshot
from runtime.project_landscape_assembly import ProjectLandscape, LandscapeSource
from runtime.project_landscape_loader import LoadedSource
from runtime.protocol_input import create_protocol_input
from runtime.source_registry import SourceRef


def make_context():
    ref = SourceRef("design.a", "design", "design/a.yaml", "active", "primary")
    loaded = LoadedSource(ref, {"opaque": True})
    landscape = ProjectLandscape(
        sources=(LandscapeSource(loaded),),
        unresolved_questions=("unknown remains",),
    )
    return create_context_snapshot(
        landscape,
        context_id="ctx-1",
        parent_landscape_ref="landscape-1",
        requested_context="writer",
    )


def test_protocol_input_preserves_context_boundary():
    context = make_context()
    protocol_input = create_protocol_input(context)

    assert protocol_input.context_id == context.context_id
    assert protocol_input.parent_landscape_ref == context.parent_landscape_ref
    assert protocol_input.source_refs is context.source_refs
    assert protocol_input.unresolved_questions == context.unresolved_questions
    assert protocol_input.requested_context == "writer"


def test_protocol_input_rejects_missing_identity():
    context = make_context()
    invalid = type(context)(
        context_id="",
        parent_landscape_ref=context.parent_landscape_ref,
        source_refs=context.source_refs,
        unresolved_questions=context.unresolved_questions,
        requested_context=context.requested_context,
    )

    with pytest.raises(ValueError):
        create_protocol_input(invalid)
