from reviewer.aiwitness_bridge import as_comparative_trace_context, as_trace_context as reviewer_trace_context, build_comparative_trace_metadata, build_trace_metadata
from reviewer.comparative_trace import as_trace_context, build_comparative_trace
from reviewer.registry import ReviewSubmission, Reviewer, ReviewerBundle


def test_comparative_trace_can_be_issued_as_aiwitness_context() -> None:
    bundle = ReviewerBundle(project_id="project-compare-1")
    bundle.register(Reviewer("reviewer-a", "matome: perspective-a"))
    bundle.register(Reviewer("reviewer-b", "matome: perspective-b"))
    submission_a = ReviewSubmission(
        "reviewer-a",
        {"finding": "x"},
        ("E1", "E2"),
        {"proposal": "A"},
    )
    submission_b = ReviewSubmission(
        "reviewer-b",
        {"finding": "y"},
        ("E1", "E3"),
        {"proposal": "B"},
    )
    bundle.submit(submission_a)
    bundle.submit(submission_b)

    comparative = build_comparative_trace(bundle)
    context = as_trace_context(comparative)
    assert context["shared_evidence_ids"] == ["E1"]
    assert context["divergent_evidence_ids"] == ["E2", "E3"]
    assert context["decision"] is None
    assert context["human_gate_required"] is True

    metadata = build_trace_metadata(bundle, submission_a)
    trace_context = reviewer_trace_context(metadata)
    assert trace_context["reviewer_id"] == "reviewer-a"
    assert trace_context["evidence_ids"] == ["E1", "E2"]
    assert trace_context["authority_granted"] is False
    assert trace_context["decision_authorized"] is False
    assert trace_context["human_gate_required"] is True

    # Comparative data remains a context payload; it does not become a decision.
    assert context["decision"] is None

    metadata = build_comparative_trace_metadata(comparative)
    witness_context = as_comparative_trace_context(metadata)
    assert witness_context["shared_evidence_ids"] == ["E1"]
    assert witness_context["divergent_evidence_ids"] == ["E2", "E3"]
    assert witness_context["decision"] is None
    assert witness_context["authority_granted"] is False
    assert witness_context["decision_authorized"] is False
    assert witness_context["human_gate_required"] is True

