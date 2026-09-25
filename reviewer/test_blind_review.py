from reviewer.blind_review import ingest_blind_review
from reviewer.registry import ReviewerBundle


def valid_result():
    return {
        "reviewer_id": "copilot-independent-alpha",
        "matome_yaml": "matome:\n  reviewer_id: copilot-independent-alpha\n",
        "observations": ["observed boundary"],
        "evidence_ids": ["E1"],
        "resolved_questions": [],
        "unresolved_questions": ["Q1"],
        "falsifiable_points": ["F1"],
        "proposals": ["P1"],
        "interpretation": ["I1"],
    }


def test_ingest_blind_review_preserves_observation_boundary():
    bundle = ReviewerBundle(project_id="blind-review-project")
    result = ingest_blind_review(bundle, valid_result())

    assert result["decision"] is None
    assert result["human_gate_required"] is True
    assert result["authority_granted"] is False
    assert result["decision_authorized"] is False
    assert result["evidence_accepted"] is False

    view = bundle.comparable_view()
    assert view["decision"] is None
    assert view["human_gate_required"] is True
    assert view["submissions"][0]["evidence_ids"] == ["E1"]
    assert view["submissions"][0]["proposal"] == {"items": ["P1"]}


def test_ingest_blind_review_rejects_invalid_result_before_ingestion():
    bundle = ReviewerBundle(project_id="blind-review-project")
    result = valid_result()
    result.pop("observations")
    try:
        ingest_blind_review(bundle, result)
    except ValueError as exc:
        assert "observations" in str(exc)
    else:
        raise AssertionError("invalid blind review must be rejected before ingestion")
    assert bundle.reviewers == {}
    assert bundle.submissions == []


def test_ingest_blind_review_preserves_questions_and_interpretation_as_observation():
    bundle = ReviewerBundle(project_id="blind-review-project")
    ingest_blind_review(bundle, valid_result())

    observation = bundle.submissions[0].observation
    assert observation["resolved_questions"] == []
    assert observation["unresolved_questions"] == ["Q1"]
    assert observation["falsifiable_points"] == ["F1"]
    assert observation["interpretation"] == ["I1"]


def test_blind_reviews_flow_into_comparative_context_without_authority():
    from reviewer.blind_review import ingest_and_compare_blind_reviews

    first = valid_result()
    second = valid_result()
    first["reviewer_id"] = "reviewer-a"
    first["matome_yaml"] = "matome:\n  reviewer_id: reviewer-a\n"
    first["evidence_ids"] = ["E1", "E2"]
    first["proposals"] = ["P1"]
    second["reviewer_id"] = "reviewer-b"
    second["matome_yaml"] = "matome:\n  reviewer_id: reviewer-b\n"
    second["evidence_ids"] = ["E1", "E3"]
    second["proposals"] = ["P2"]

    context = ingest_and_compare_blind_reviews(
        ReviewerBundle(project_id="blind-review-project"),
        [first, second],
    )

    assert context["shared_evidence_ids"] == ["E1"]
    assert context["divergent_evidence_ids"] == ["E2", "E3"]
    assert context["decision"] is None
    assert context["authority_granted"] is False
    assert context["decision_authorized"] is False
    assert context["human_gate_required"] is True
    assert [item["proposal"] for item in context["observations"]] == [
        {"items": ["P1"]},
        {"items": ["P2"]},
    ]
