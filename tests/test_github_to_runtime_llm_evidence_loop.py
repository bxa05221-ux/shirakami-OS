from runtime.adapter import PipelineAdapter
from runtime.evidence import capture_evidence
from runtime.github_landscape_adapter import FakeGitHubClient, GitHubLandscapeAdapter
from runtime.github_protocol_loader import GitHubProtocolLoader
from runtime.pipeline import build_pipeline_plan
from runtime.pipeline_execution import execute_pipeline_plan
from runtime.protocol_api import build_protocol_request
from runtime.protocol_bridge import protocol_from_ir
from runtime.protocol_registry import ProtocolRegistry
from runtime.prototype import Runtime


PROTOCOL_YAML = """\
matome:
  title: GitHub to Shirakami minimum path
  version: "0.1"
  statement: >
    Observe a GitHub-hosted protocol through the existing Runtime boundary.
pipeline:
  - phase: observe
    action: inspect
  - phase: respond
    action: formulate
"""


class FakeGitHubContentsClient:
    def get(self, path):
        assert path == "protocols/minimum-path.yaml"
        return {"content": PROTOCOL_YAML}


def _load_protocol():
    return GitHubProtocolLoader(FakeGitHubContentsClient()).load(
        "protocols/minimum-path.yaml"
    )


def _run_with_backend(protocol, backend_id, output):
    plan = build_pipeline_plan(protocol, {"source": "github"})
    registry = ProtocolRegistry()
    registry.register_temporary(protocol.protocol_id, protocol)
    request = build_protocol_request(
        registry,
        protocol.protocol_id,
        {"human_gate": "pending"},
    )
    adapter = PipelineAdapter(lambda request: output, backend_id=backend_id)
    return execute_pipeline_plan(request, plan, adapter)


def test_github_protocol_reaches_runtime_evidence_and_landscape():
    protocol = _load_protocol()
    trace = _run_with_backend(
        protocol,
        "llm-a",
        {"response": "deterministic-model-output"},
    )

    execution = Runtime().execute(
        protocol.protocol_id,
        protocol_from_ir(protocol),
        {
            "human_gate": "pending",
            "adapter_backend": trace.backends[-1],
            "adapter_output": trace.steps[-1].output["response"],
        },
    )
    evidence = capture_evidence(execution)

    github = FakeGitHubClient({"human_gate": "pending"})
    landscape = GitHubLandscapeAdapter(github)
    landscape.apply_transition(evidence)

    state = landscape.read_state()

    assert trace.completed is True
    assert trace.backends == ("llm-a", "llm-a")
    assert evidence.protocol_id == protocol.protocol_id
    assert state["input"]["adapter_output"] == "deterministic-model-output"
    assert state["input"]["adapter_backend"] == "llm-a"
    assert state["input"]["human_gate"] == "pending"
    assert "judgment" not in state
    assert "decision" not in state


def test_same_github_protocol_preserves_boundary_when_llm_backend_changes():
    protocol = _load_protocol()
    trace_a = _run_with_backend(protocol, "llm-a", {"response": "A"})
    trace_b = _run_with_backend(protocol, "llm-b", {"response": "B"})

    assert trace_a.protocol_id == trace_b.protocol_id == protocol.protocol_id
    assert trace_a.version == trace_b.version == protocol.version
    assert trace_a.backends == ("llm-a", "llm-a")
    assert trace_b.backends == ("llm-b", "llm-b")
    assert [step.evidence["action"] for step in trace_a.steps] == [
        step.evidence["action"] for step in trace_b.steps
    ]
    assert trace_a.steps[-1].output != trace_b.steps[-1].output
