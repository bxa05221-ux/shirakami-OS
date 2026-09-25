from reviewer.reviewer import ReviewerBundle, ReviewerPerspective


def test_multiple_reviewer_perspectives_remain_comparable_without_consensus() -> None:
    bundle = ReviewerBundle(
        project="Shirakami",
        objective="compare reviewer observations",
        evidence_ids=("E-1", "E-2"),
        reviewers=(
            ReviewerPerspective("reviewer-a", "runtime", {"goal": "safety"}, ("boundary preserved",), ("E-1",), ("keep gate",)),
            ReviewerPerspective("reviewer-b", "creative", {"goal": "usability"}, ("context remains legible",), ("E-2",), ("add renderer",)),
        ),
    )
    result = bundle.compare()
    assert len(result["reviewers"]) == 2
    assert result["decision"] is None
    assert result["human_gate_required"] is True
    assert all(item["execution_authorized"] is False for item in result["reviewers"])
