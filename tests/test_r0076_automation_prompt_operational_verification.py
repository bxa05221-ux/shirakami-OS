from pathlib import Path


PROMPT = Path("docs/operations/automation-prompt-v2.md")
WORKFLOW = Path(".github/workflows/operation-execution.yml")


def test_automation_prompt_v2_exists_and_declares_scope():
    text = PROMPT.read_text(encoding="utf-8")
    assert "Automation Prompt v2.0" in text
    assert "Scope: implementation and operation only" in text
    assert "not a Protocol" in text
    assert "not a source of domain truth" in text


def test_automation_prompt_v2_declares_canonical_execution_shape():
    text = PROMPT.read_text(encoding="utf-8")
    expected = [
        "Operation",
        "Baseline",
        "Branch",
        "Artifact",
        "Verification",
        "Protected PR",
        "Protected Merge",
        "Main Verification",
        "Operation Result",
    ]
    for item in expected:
        assert item in text


def test_automation_prompt_v2_declares_execution_identity_and_mismatch_rule():
    text = PROMPT.read_text(encoding="utf-8")
    assert "Execution ID identifies one execution instance." in text
    assert "Result identity is `(Operation ID, Execution ID)`." in text
    assert "do not guess" in text
    assert "reported merge SHA" in text


def test_execution_workflow_matches_prompt_runtime_boundaries():
    text = WORKFLOW.read_text(encoding="utf-8")
    for required in (
        "runtime.operation_runner",
        "runtime.operation_replay",
        "execution_branch",
        "execution_artifact",
        "python -m pytest runtime tests -q",
        "gh pr create",
    ):
        assert required in text
    assert "gh pr merge" not in text
    assert "merge_pull_request" not in text
