from runtime.pipeline import build_pipeline_plan
from runtime.protocol_loader import parse_matome


def test_pipeline_is_derived_from_selected_protocol():
    protocol = parse_matome(
        """matome:
  title: "文章作成"
  version: "0.1"
  statement: >
    文章を整理して編集する。
  pipeline:
    - phase: observe
      action: inspect
    - phase: organize
      action: structure
"""
    )

    plan = build_pipeline_plan(protocol, {"time": "night"})

    assert plan.protocol_id == protocol.protocol_id
    assert plan.version == "0.1"
    assert [(step.phase, step.action) for step in plan.steps] == [
        ("observe", "inspect"),
        ("organize", "structure"),
    ]
    assert plan.context["time"] == "night"


def test_pipeline_does_not_select_backend():
    protocol = parse_matome(
        """matome:
  title: "証拠整理"
  version: "0.1"
  statement: >
    Evidenceを整理する。
  pipeline:
    - phase: observe
      action: inspect
"""
    )

    plan = build_pipeline_plan(protocol)

    assert not hasattr(plan, "backend")
    assert not hasattr(plan, "model")
