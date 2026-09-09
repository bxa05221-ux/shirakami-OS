from pathlib import Path


WORKFLOW = Path(".github/workflows/operation-execution.yml")


def test_r0073_workflow_has_declared_execution_boundaries():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "workflow_dispatch:" in text
    assert "contents: write" in text
    assert "pull-requests: write" in text
    assert "plan_operation" in text
    assert "git switch -c" in text
    assert "git push --set-upstream origin" in text
    assert "gh pr create" in text
    assert "python -m pytest runtime tests -q" in text


def test_r0073_workflow_does_not_merge_pull_requests():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "gh pr merge" not in text
    assert "merge_pull_request" not in text


def test_r0073_workflow_keeps_canonical_verification_explicit():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "Run canonical verification" in text
    assert "test-runtime" in text
