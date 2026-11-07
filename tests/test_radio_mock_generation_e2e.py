"""Offline R1 regression tests for Radio v2.1 draft generation.

The speech evaluation is intentionally limited lexical heuristic coverage. It
detects only the fixture risks below and makes no quality or broad compliance
guarantee.  No test invokes a provider, publishes, or mutates Reality.
"""

from runtime.adapter import PipelineAdapter
from runtime.guide_thread import (
    build_guide_thread_requests,
    execute_selected_runtime_candidate,
    propose_runtime_candidate,
    select_runtime_candidate,
)
from runtime.model_response_observation import observe_model_response
from runtime.oppai_runtime_flow import build_selected_protocol_request
from runtime.pipeline import build_pipeline_plan
from runtime.protocol_loader import ProtocolIR
from runtime.protocol_registry import ProtocolRegistry
from runtime.radio_speech_evaluation import evaluate_radio_speech
from runtime.real_model_adapter import RealModelAdapter


def _radio_setup():
    registry = ProtocolRegistry()
    artifact = ProtocolIR(
        protocol_id="shirakami-radio-v2.1",
        title="Shirakami Radio Cognitive Edition",
        version="2.1.0",
        statement="Independent landscapes without advice or semantic bridging.",
        pipeline=({"phase": "listener", "action": "generate_independent_landscape"},),
    )
    registry.register_temporary(artifact.protocol_id, artifact)
    control = {
        "source_kind": "listener_letter",
        "consent_scope": "session_only",
        "broadcast_authorized": False,
        "listener_count": 2,
        "restrictions": {
            "advice": False,
            "analysis": False,
            "semantic_bridging": False,
            "reality_mutation": False,
        },
    }
    protocol_request = build_selected_protocol_request(
        "今朝、新聞を配る途中で風が冷たかったです。",
        registry,
        artifact.protocol_id,
        context={"generation_control": control, "broadcast_authorized": False},
    )
    plan = build_pipeline_plan(
        registry.select_current(artifact.protocol_id).artifact,
        context={"generation_control": control, "broadcast_authorized": False},
    )
    return artifact, control, build_guide_thread_requests(protocol_request, plan)[0]


def test_mock_generation_e2e_preserves_control_observes_output_and_never_requeues():
    artifact, original_control, guide_request = _radio_setup()
    captured = []
    model_output = {
        "listeners": [
            "雨上がりの駅で、傘の先から小さな雫が落ちていました。",
            "台所でコーヒーをいれて、湯気を少し眺めていました。",
        ],
        "personality": ["風の音が、今日は少し近くに聞こえますね。"],
    }
    real_model = RealModelAdapter(lambda request: captured.append(request) or model_output)
    candidate = propose_runtime_candidate(guide_request)

    result = execute_selected_runtime_candidate(
        select_runtime_candidate(candidate),
        PipelineAdapter(real_model.execute_pipeline, backend_id="offline-fixture"),
    )
    pending = observe_model_response(result, candidate)

    assert result.output is model_output
    assert len(captured) == 1
    sent_control = captured[0].context["generation_control"]
    assert sent_control["source_kind"] == "listener_letter"
    assert sent_control["consent_scope"] == "session_only"
    assert sent_control["broadcast_authorized"] is False
    assert sent_control["restrictions"] == original_control["restrictions"]
    assert sent_control["protocol_id"] == artifact.protocol_id
    assert sent_control["protocol_version"] == artifact.version
    assert sent_control["phase"] == "listener"
    assert sent_control["action"] == "generate_independent_landscape"
    assert "publish_authorized" not in captured[0].context
    assert original_control["restrictions"]["reality_mutation"] is False

    assert pending.evidence.transition_kind == "model.response.observed"
    assert pending.evidence.transition_data["output"] is model_output
    assert pending.auto_execute is False
    assert pending.authority == "not_inferred"
    assert not hasattr(pending, "execute")
    assert len(captured) == 1


def test_limited_speech_heuristics_flag_duplicate_scenery_advice_analysis_and_bridging():
    evaluation = evaluate_radio_speech(
        [
            "駅のホームに雨の匂いが残っていました。",
            "改札のそばで、濡れた傘をたたみました。",
        ],
        [
            "気持ちを分析すると、休んだほうがよさそうです。",
            "どちらも同じことを教えてくれる投稿ですね。",
        ],
    )

    assert evaluation.duplicate_landscape_pairs == (
        (0, 1, "rain"),
        (0, 1, "station"),
    )
    assert evaluation.personality_restriction_hits == (
        "気持ちを分析すると、休んだほうがよさそうです。",
    )
    assert evaluation.semantic_bridge_hits == (
        "どちらも同じことを教えてくれる投稿ですね。",
    )
    assert "does not guarantee" in evaluation.limitation


def test_limited_speech_heuristics_leave_distinct_non_advisory_fixture_unflagged():
    evaluation = evaluate_radio_speech(
        [
            "雨上がりの駅で、傘の先から小さな雫が落ちていました。",
            "台所でコーヒーをいれて、湯気を少し眺めていました。",
        ],
        ["風の音が、今日は少し近くに聞こえますね。"],
    )

    assert evaluation.duplicate_landscape_pairs == ()
    assert evaluation.personality_restriction_hits == ()
    assert evaluation.semantic_bridge_hits == ()
