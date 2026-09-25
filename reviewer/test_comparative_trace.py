from reviewer.comparative_trace import as_trace_context, build_comparative_trace
from reviewer.registry import ReviewSubmission, Reviewer, ReviewerBundle


def test_comparative_trace_preserves_shared_and_divergent_evidence() -> None:
    bundle = ReviewerBundle(project_id="project-1")
    bundle.register(Reviewer("reviewer-a", "matome: a"))
    bundle.register(Reviewer("reviewer-b", "matome: b"))
    bundle.submit(ReviewSubmission("reviewer-a", {"finding": "x"}, ("E1", "E2"), {"next": "A"}))
    bundle.submit(ReviewSubmission("reviewer-b", {"finding": "y"}, ("E1", "E3"), {"next": "B"}))

    trace = build_comparative_trace(bundle)
    assert trace.shared_evidence_ids == ("E1",)
    assert trace.divergent_evidence_ids == ("E2", "E3")
    assert len(trace.observations) == 2
    assert trace.human_gate_required is True
    assert trace.decision is None


def test_comparative_trace_with_one_reviewer_keeps_all_evidence_divergent() -> None:
    bundle = ReviewerBundle(project_id="project-1")
    bundle.register(Reviewer("reviewer-a", "matome: a"))
    bundle.submit(ReviewSubmission("reviewer-a", {"finding": "x"}, ("E1", "E2")))

    trace = build_comparative_trace(bundle)
    assert trace.shared_evidence_ids == ()
    assert trace.divergent_evidence_ids == ("E1", "E2")


def test_trace_context_has_no_decision_authority() -> None:
    bundle = ReviewerBundle(project_id="project-1")
    bundle.register(Reviewer("reviewer-a", "matome: a"))
    bundle.register(Reviewer("reviewer-b", "matome: b"))
    bundle.submit(ReviewSubmission("reviewer-a", {"finding": "x"}, ("E1",)))
    bundle.submit(ReviewSubmission("reviewer-b", {"finding": "y"}, ("E1", "E2")))

    context = as_trace_context(build_comparative_trace(bundle))
    assert context["shared_evidence_ids"] == ["E1"]
    assert context["divergent_evidence_ids"] == ["E2"]
    assert context["human_gate_required"] is True
    assert context["decision"] is None
