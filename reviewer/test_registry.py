import pytest

from reviewer.registry import ReviewSubmission, Reviewer, ReviewerBundle


def test_reviewer_bundle_preserves_distinct_perspectives() -> None:
    bundle = ReviewerBundle(project_id="project-1")
    bundle.register(Reviewer("reviewer-a", "matome: a", {"role": "research"}))
    bundle.register(Reviewer("reviewer-b", "matome: b", {"role": "review"}))

    bundle.submit(ReviewSubmission("reviewer-a", {"finding": "x"}, ("E-A",), {"proposal": "A"}))
    bundle.submit(ReviewSubmission("reviewer-b", {"finding": "y"}, ("E-B",), {"proposal": "B"}))

    view = bundle.comparable_view()
    assert [r["reviewer_id"] for r in view["reviewers"]] == ["reviewer-a", "reviewer-b"]
    assert [s["reviewer_id"] for s in view["submissions"]] == ["reviewer-a", "reviewer-b"]
    assert view["decision"] is None
    assert view["human_gate_required"] is True


def test_unregistered_reviewer_cannot_submit() -> None:
    bundle = ReviewerBundle(project_id="project-1")
    try:
        bundle.submit(ReviewSubmission("unknown", {}, ()))
    except ValueError as exc:
        assert "registered" in str(exc)
    else:
        raise AssertionError("unregistered reviewer submission must be rejected")


def test_invalid_matome_yaml_is_rejected() -> None:
    bundle = ReviewerBundle(project_id="project-1")
    with pytest.raises(ValueError, match="valid YAML"):
        bundle.register(Reviewer("reviewer-a", "matome: ["))


def test_matome_yaml_must_be_a_mapping() -> None:
    bundle = ReviewerBundle(project_id="project-1")
    with pytest.raises(ValueError, match="YAML mapping"):
        bundle.register(Reviewer("reviewer-a", "- not-a-mapping"))


def test_empty_matome_yaml_is_rejected() -> None:
    bundle = ReviewerBundle(project_id="project-1")
    with pytest.raises(ValueError, match="matome_yaml is required"):
        bundle.register(Reviewer("reviewer-a", ""))
