from pathlib import Path

from runtime.adapter import PipelineAdapter
from runtime.evidence import capture_evidence
from runtime.local_repository_loader import LocalRepositoryProtocolLoader
from runtime.landscape import LandscapeState
from runtime.pipeline import build_pipeline_plan
from runtime.pipeline_execution import execute_pipeline_plan
from runtime.protocol_api import build_protocol_request
from runtime.protocol_bridge import protocol_from_ir
from runtime.prototype import Runtime
from runtime.protocol_registry import ProtocolRegistry


PROTOCOL_YAML = """\
matome:
  title: Shirakami LLM Evidence Loop
  version: "0.1"
  statement: >
    Execute a local protocol through a replaceable backend and record the execution boundary.
pipeline:
  - phase: observe
    action: inspect
  - phase: respond
    action: formulate
"""


def test_local_repository_llm_response_reaches_evidence_without_becoming_authority(tmp_path: Path):
    path = tmp_path / "protocol.yaml"
    path.write_text(PROTOCOL_YAML, encoding="utf-8")
    protocol = LocalRepositoryProtocolLoader(tmp_path).load("protocol.yaml")

    plan = build_pipeline_plan(protocol, {"landscape": "local"})
    registry = ProtocolRegistry()
    registry.register_temporary(protocol.protocol_id, protocol)
    request = build_protocol_request(
        registry,
        protocol.protocol_id,
        {"human_gate": "pending"},
    )

    adapter = PipelineAdapter(
        lambda req: {"response": "deterministic-model-output", "human_gate": req.input["human_gate"]},
        backend_id="llm-a",
    )
    trace = execute_pipeline_plan(request, plan, adapter)

    runtime_protocol = protocol_from_ir(protocol)
    execution = Runtime().execute(
        protocol.protocol_id,
        runtime_protocol,
        {
            "human_gate": "pending",
            "adapter_backend": trace.backends[0],
            "adapter_output": trace.steps[-1].output["response"],
        },
    )
    evidence = capture_evidence(execution)

    landscape = LandscapeState.from_snapshot({"owner": "human"})
    landscape.apply_evidence(evidence)

    assert trace.completed is True
    assert trace.backends == ("llm-a", "llm-a")
    assert evidence.protocol_id == protocol.protocol_id
    assert evidence.transition_data["input"]["adapter_output"] == "deterministic-model-output"
    assert evidence.transition_data["input"]["adapter_backend"] == "llm-a"
    assert evidence.transition_data["input"]["human_gate"] == "pending"
    assert landscape.snapshot()["adapter_output"] == "deterministic-model-output"
    assert "judgment" not in landscape.snapshot()
    assert "decision" not in landscape.snapshot()


def test_same_local_protocol_preserves_evidence_boundary_when_backend_changes(tmp_path: Path):
    path = tmp_path / "protocol.yaml"
    path.write_text(PROTOCOL_YAML, encoding="utf-8")
    protocol = LocalRepositoryProtocolLoader(tmp_path).load("protocol.yaml")
    plan = build_pipeline_plan(protocol, {"landscape": "local"})
    registry = ProtocolRegistry()
    registry.register_temporary(protocol.protocol_id, protocol)
    request = build_protocol_request(registry, protocol.protocol_id, {"human_gate": "pending"})

    def run(backend_id, output):
        adapter = PipelineAdapter(lambda req: output, backend_id=backend_id)
        return execute_pipeline_plan(request, plan, adapter)

    trace_a = run("llm-a", {"response": "A"})
    trace_b = run("llm-b", {"response": "B"})

    assert trace_a.protocol_id == trace_b.protocol_id == protocol.protocol_id
    assert trace_a.version == trace_b.version == protocol.version
    assert trace_a.backends == ("llm-a", "llm-a")
    assert trace_b.backends == ("llm-b", "llm-b")
    assert [s.evidence["action"] for s in trace_a.steps] == [s.evidence["action"] for s in trace_b.steps]
    assert trace_a.steps[-1].output != trace_b.steps[-1].output