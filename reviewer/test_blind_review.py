from reviewer.blind_review import ingest_blind_review
from reviewer.registry import ReviewerBundle


def valid_result():
    return {
        "reviewer_id": "copilot-independent-alpha",
        "matome_yaml": "matome:\n  reviewer_id: copilot-independent-alpha\n",
"human_gate": {"required": True, "decision": "pending"},
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


def test_blind_review_comparative_context_passes_aiwitness_traceability():
    from aiwitness.traceability import validate_comparative_traceability
    from reviewer.blind_review import ingest_and_compare_blind_reviews

    first = valid_result()
    second = valid_result()
    first.update({
        "reviewer_id": "reviewer-a",
        "matome_yaml": "matome:\n  reviewer_id: reviewer-a\n",
        "evidence_ids": ["E1", "E2"],
        "proposals": ["P1"],
    })
    second.update({
        "reviewer_id": "reviewer-b",
        "matome_yaml": "matome:\n  reviewer_id: reviewer-b\n",
        "evidence_ids": ["E1", "E3"],
        "proposals": ["P2"],
    })

    context = ingest_and_compare_blind_reviews(
        ReviewerBundle(project_id="blind-review-traceability"),
        [first, second],
    )
    record = validate_comparative_traceability(context=context)

    assert record.project_id == "blind-review-traceability"
    assert record.reviewer_ids == ("reviewer-a", "reviewer-b")
    assert record.shared_evidence_ids == ("E1",)
    assert record.divergent_evidence_ids == ("E2", "E3")
    assert record.decision is None
    assert record.authority_granted is False
    assert record.decision_authorized is False
    assert record.human_gate_required is True
