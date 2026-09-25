from reviewer.aiwitness_bridge import build_trace_metadata
from reviewer.comparative_trace import as_trace_context, build_comparative_trace
from reviewer.registry import ReviewSubmission, Reviewer, ReviewerBundle


def test_comparative_trace_can_be_issued_as_aiwitness_context() -> None:
    bundle = ReviewerBundle(project_id="project-compare-1")
    bundle.register(Reviewer("reviewer-a", "matome: perspective-a"))
    bundle.register(Reviewer("reviewer-b", "matome: perspective-b"))
    bundle.submit(
        ReviewSubmission(
            "reviewer-a",
            {"finding": "x"},
            ("E1", "E2"),
            {"proposal": "A"},
        )
    )
    bundle.submit(
        ReviewSubmission(
            "reviewer-b",
            {"finding": "y"},
            ("E1", "E3"),
            {"proposal": "B"},
        )
    )

    comparative = build_comparative_trace(bundle)
    context = as_trace_context(comparative)
    assert context["shared_evidence_ids"] == ["E1"]
    assert context["divergent_evidence_ids"] == ["E2", "E3"]
    assert context["decision"] is None
    assert context["human_gate_required"] is True

    metadata = build_trace_metadata(
        reviewer_id="comparative-review",
        evidence_ids=("E1", "E2", "E3"),
        matome_yaml="comparative-review",
        trace_role="multi-agent-comparative-review",
    )
    trace_context = metadata.as_trace_context()
    assert trace_context["reviewer_id"] == "comparative-review"
    assert trace_context["evidence_ids"] == ["E1", "E2", "E3"]
    assert trace_context["authority_granted"] is False
    assert trace_context["decision_authorized"] is False
    assert trace_context["human_gate_required"] is True

    # Comparative data remains a context payload; it does not become a decision.
    assert context["decision"] is None
