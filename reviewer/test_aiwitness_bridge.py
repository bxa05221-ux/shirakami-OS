from reviewer.aiwitness_bridge import as_trace_context, build_trace_metadata
from reviewer.registry import ReviewSubmission, Reviewer, ReviewerBundle


def test_reviewer_metadata_can_become_trace_context_without_authority() -> None:
    bundle = ReviewerBundle(project_id="project-1")
    bundle.register(Reviewer("reviewer-a", "matome: a"))
    submission = ReviewSubmission(
        reviewer_id="reviewer-a",
        observation={"finding": "x"},
        evidence_ids=("E-1", "E-2"),
        proposal={"next": "inspect"},
    )

    metadata = build_trace_metadata(bundle, submission)
    context = as_trace_context(metadata)

    assert context["reviewer_id"] == "reviewer-a"
    assert context["evidence_ids"] == ["E-1", "E-2"]
    assert context["matome_yaml"] == "matome: a"
    assert context["authority_granted"] is False
    assert context["decision_authorized"] is False
    assert context["human_gate_required"] is True


def test_unregistered_reviewer_cannot_enter_trace_context() -> None:
    bundle = ReviewerBundle(project_id="project-1")
    submission = ReviewSubmission("unknown", {}, ("E-1",))

    try:
        build_trace_metadata(bundle, submission)
    except ValueError as exc:
        assert "registered" in str(exc)
    else:
        raise AssertionError("unregistered reviewer must be rejected")
