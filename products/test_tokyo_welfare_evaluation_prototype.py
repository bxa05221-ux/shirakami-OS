import pytest

from products.tokyo_welfare_evaluation_prototype import (
    ConsensusRecord, EvaluatorInput, SyntheticCase, TokyoWelfareEvaluationTrial,
    TrialBoundaryError, TrialFeedback,
)


def trial():
    return TokyoWelfareEvaluationTrial(
        SyntheticCase("synthetic-case-1", "架空事業所", "架空サービス", "架空シナリオ"),
        {"a", "b"},
    )


def input_for(evaluator_id, evidence):
    return EvaluatorInput(evaluator_id, "基準", "架空の観察", tuple(evidence), "暫定的見解")


def test_end_to_end_trial_preserves_difference_and_requires_human_consensus():
    workflow = trial()
    first = workflow.record_input(input_for("a", ("E-1", "E-2")))
    second = workflow.record_input(input_for("b", ("E-1", "E-3")))
    workflow.share_for_consensus(first, "a")
    workflow.share_for_consensus(second, "b")
    comparison = workflow.compare_views()
    assert comparison["shared_evidence"] == ["E-1"]
    assert comparison["divergent_evidence"] == ["E-2", "E-3"]
    assert comparison["decision"] is None
    with pytest.raises(TrialBoundaryError, match="human evaluator"):
        workflow.record_human_consensus(ConsensusRecord("a", "automated", (), False))
    workflow.record_human_consensus(ConsensusRecord("a", "人間が記録した合議", ("未解決事項",), True))
    report = workflow.draft_report()
    assert report["synthetic_only"] is True
    assert report["status"] == "DRAFT - human review required"
    assert report["final_decision"] is None
    assert report["human_consensus"]["note"] == "人間が記録した合議"


def test_real_or_unshared_input_is_rejected_or_hidden():
    with pytest.raises(TrialBoundaryError, match="synthetic"):
        TokyoWelfareEvaluationTrial(SyntheticCase("case-1", "事業所", "サービス", "scenario", False), {"a"})
    with pytest.raises(TrialBoundaryError, match="synthetic"):
        TokyoWelfareEvaluationTrial(SyntheticCase("case-1", "架空事業所", "架空サービス", "架空シナリオ"), {"a"})
    workflow = trial()
    private_id = workflow.record_input(input_for("a", ("E-1",)))
    assert workflow.compare_views()["views"] == []
    with pytest.raises(TrialBoundaryError, match="unknown"):
        workflow.share_for_consensus("not-a-record", "a")
    workflow.share_for_consensus(private_id, "a")
    assert len(workflow.compare_views()["views"]) == 1


def test_feedback_is_collected_without_authority_change():
    workflow = trial()
    workflow.submit_feedback(TrialFeedback("a", 3, "根拠整理", "表示", "検討する"))
    assert workflow.feedback_summary()[0]["ease_of_use"] == 3
    with pytest.raises(TrialBoundaryError, match="between"):
        workflow.submit_feedback(TrialFeedback("a", 6, "x", "y", "z"))
