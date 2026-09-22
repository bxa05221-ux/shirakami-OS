from pathlib import Path

from runtime.adapter import PipelineAdapter, PipelineAdapterRequest
from runtime.local_repository_loader import LocalRepositoryProtocolLoader
from runtime.pipeline import build_pipeline_plan


PROTOCOL_YAML = """\
matome:
  title: SHIRAKAMI REPLACEABLE LLM
  version: "0.1"
  statement: >
    The same protocol remains active while the execution backend changes.
pipeline:
  - phase: observe
    action: inspect
  - phase: respond
    action: formulate
"""


def _write_protocol(root: Path) -> str:
    path = root / "protocols" / "replaceable-llm.yaml"
    path.parent.mkdir(parents=True)
    path.write_text(PROTOCOL_YAML, encoding="utf-8")
    return "protocols/replaceable-llm.yaml"


def _run_backend(protocol, backend_id, label):
    plan = build_pipeline_plan(protocol, {"landscape": "local"})
    adapter = PipelineAdapter(
        lambda request: {
            "backend": label,
            "protocol_id": request.protocol_id,
            "phase": request.phase,
            "action": request.action,
        },
        backend_id=backend_id,
    )

    results = []
    for step in plan.steps:
        results.append(
            adapter.execute(
                PipelineAdapterRequest(
                    protocol_id=plan.protocol_id,
                    version=plan.version,
                    phase=step.phase,
                    action=step.action,
                    input={"human_gate": "pending"},
                    context=plan.context,
                )
            )
        )
    return plan, results


def test_local_repository_keeps_protocol_stable_across_replaceable_backends(tmp_path: Path):
    protocol_path = _write_protocol(tmp_path)
    protocol = LocalRepositoryProtocolLoader(tmp_path).load(protocol_path)

    plan_a, results_a = _run_backend(protocol, "llm-a", "model-a")
    plan_b, results_b = _run_backend(protocol, "llm-b", "model-b")

    assert plan_a == plan_b
    assert [result.evidence["protocol_id"] for result in results_a] == [
        protocol.protocol_id
    ] * len(results_a)
    assert [result.evidence["action"] for result in results_a] == [
        result.evidence["action"] for result in results_b
    ]
    assert [result.backend for result in results_a] == ["llm-a", "llm-a"]
    assert [result.backend for result in results_b] == ["llm-b", "llm-b"]
    assert [result.output["backend"] for result in results_a] == [
        "model-a",
        "model-a",
    ]
    assert [result.output["backend"] for result in results_b] == [
        "model-b",
        "model-b",
    ]
    assert all(
        result.output["protocol_id"] == protocol.protocol_id
        for result in results_a + results_b
    )
    assert all(
        result.output["action"] in {"inspect", "formulate"}
        for result in results_a + results_b
    )
