import pytest

from runtime.adapter import PipelineAdapter
from runtime.guide_thread import (
    GuideThreadError,
    build_guide_thread_requests,
    execute_selected_runtime_candidate,
    propose_runtime_candidate,
    select_runtime_candidate,
)
from runtime.model_response_observation import observe_model_response
from runtime.oppai_runtime_flow import build_selected_protocol_request
from runtime.pipeline import build_pipeline_plan
from runtime.protocol_api import register_temporary_matome
from runtime.protocol_registry import ProtocolRegistry


def _prepared_guide_request():
    registry = ProtocolRegistry()
    entry = register_temporary_matome(
        registry,
        '''matome:
  title: "Guide boundary"
  version: "0.1"
  statement: >
    Preserve explicit human selection.
  pipeline:
    - phase: guide
      action: draft
''',
    )
    protocol_request = build_selected_protocol_request(
        "次の案を作って",
        registry,
        entry.protocol_id,
        context={"nested": {"unchanged": True}},
    )
    plan = build_pipeline_plan(registry.select_current(entry.protocol_id).artifact, context={"channel": "radio"})
    return build_guide_thread_requests(protocol_request, plan)[0]


def test_protocol_pipeline_is_copied_to_immutable_guide_thread_request():
    request = _prepared_guide_request()

    assert (request.protocol, request.version, request.phase, request.action) == (
        "guide.boundary", "0.1", "guide", "draft"
    )
    assert request.input["canonical_prompt"] == "次の案を作って"
    with pytest.raises(TypeError):
        request.context["channel"] = "changed"


def test_only_explicitly_selected_guide_candidate_reaches_runtime():
    request = _prepared_guide_request()
    candidate = propose_runtime_candidate(request)
    seen = []
    adapter = PipelineAdapter(lambda item: seen.append(item) or "draft", backend_id="fixture")

    with pytest.raises(GuideThreadError):
        execute_selected_runtime_candidate(candidate, adapter)  # type: ignore[arg-type]
    assert seen == []

    result = execute_selected_runtime_candidate(select_runtime_candidate(candidate), adapter)
    assert result.output == "draft"
    assert [(item.phase, item.action) for item in seen] == [("guide", "draft")]


def test_model_response_becomes_observed_pending_next_turn_without_reexecution():
    request = _prepared_guide_request()
    candidate = propose_runtime_candidate(request)
    calls = []
    adapter = PipelineAdapter(lambda item: calls.append(item) or {"text": "draft"}, backend_id="fixture")
    result = execute_selected_runtime_candidate(select_runtime_candidate(candidate), adapter)

    pending = observe_model_response(result, candidate)

    assert len(calls) == 1
    assert pending.auto_execute is False
    assert pending.authority == "not_inferred"
    assert pending.evidence.transition_kind == "model.response.observed"
    assert pending.evidence.transition_data["output"] == {"text": "draft"}
    assert pending.evidence.transition_data["authority"] == "not_inferred"
    assert not hasattr(pending, "execute")
