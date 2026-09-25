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


def test_ingest_blind_review_preserves_questions_and_interpretation_as_observation():
    bundle = ReviewerBundle(project_id="blind-review-project")
    ingest_blind_review(bundle, valid_result())

    observation = bundle.submissions[0].observation
    assert observation["resolved_questions"] == []
    assert observation["unresolved_questions"] == ["Q1"]
    assert observation["falsifiable_points"] == ["F1"]
    assert observation["interpretation"] == ["I1"]
