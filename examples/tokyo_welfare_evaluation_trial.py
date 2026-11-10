"""Run the synthetic-only Tokyo welfare-service evaluation trial end to end."""
from __future__ import annotations

import json
from pathlib import Path
import sys

# Permit direct execution from a repository checkout without installation.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from products.tokyo_welfare_evaluation_prototype import (
    ConsensusRecord,
    EvaluatorInput,
    SyntheticCase,
    TokyoWelfareEvaluationTrial,
    TrialFeedback,
)


def build_demo() -> TokyoWelfareEvaluationTrial:
    trial = TokyoWelfareEvaluationTrial(
        SyntheticCase(
            case_id="synthetic-day-service-001",
            title="架空デイサービス あおば",
            service_type="通所介護（架空）",
            scenario="架空の利用者アンケートと運営記録を用いた試用シナリオ。",
        ),
        {"evaluator-a", "evaluator-b"},
    )
    first = trial.record_input(EvaluatorInput(
        "evaluator-a", "利用者本位の支援", "希望確認の記録はあるが、振り返り頻度は資料から判断できない。",
        ("E-01: 架空アンケート", "E-02: 架空支援記録"), "追加の聞き取りが必要。",
    ))
    second = trial.record_input(EvaluatorInput(
        "evaluator-b", "利用者本位の支援", "希望確認の仕組みは確認でき、職員間共有の記録もある。",
        ("E-01: 架空アンケート", "E-03: 架空会議記録"), "仕組みは機能している可能性がある。",
    ))
    trial.share_for_consensus(first, "evaluator-a")
    trial.share_for_consensus(second, "evaluator-b")
    trial.record_human_consensus(ConsensusRecord(
        "evaluator-a", "根拠の一致・相違を確認し、現地で振り返り頻度を追加確認する。",
        ("振り返りの実施頻度",), True,
    ))
    trial.submit_feedback(TrialFeedback("evaluator-a", 4, "根拠を並べて確認できた。", "共有操作の意図を最初に説明してほしい。", "条件付きで使いたい。"))
    return trial


if __name__ == "__main__":
    demo = build_demo()
    print(json.dumps({"report_draft": demo.draft_report(), "trial_feedback": demo.feedback_summary()}, ensure_ascii=False, indent=2))
