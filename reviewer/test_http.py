from reviewer.http import get_reviewers, register_reviewer, submit_review
from reviewer.registry import ReviewerBundle


def test_reviewer_http_boundary_preserves_matome_and_evidence() -> None:
    bundle = ReviewerBundle(project_id="project-http")
    assert register_reviewer(bundle, {
        "reviewer_id": "reviewer-a",
        "matome_yaml": "matome: a",
        "metadata": {"role": "research"},
    })["registered"] is True
    assert submit_review(bundle, {
        "reviewer_id": "reviewer-a",
        "observation": {"finding": "x"},
        "evidence_ids": ["E-1", "E-2"],
        "proposal": {"next": "inspect"},
    })["submitted"] is True

    view = get_reviewers(bundle)
    assert view["project_id"] == "project-http"
    assert view["reviewers"][0]["matome_yaml"] == "matome: a"
    assert view["submissions"][0]["evidence_ids"] == ["E-1", "E-2"]
    assert view["decision"] is None
    assert view["human_gate_required"] is True
