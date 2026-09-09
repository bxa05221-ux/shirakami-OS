"""Replay-safe execution naming for Shirakami OS operations."""

import re


def execution_branch(operation_id: str, execution_id: str) -> str:
    """Return a unique GitHub branch name for one execution instance."""
    if not operation_id:
        raise ValueError("operation_id is required")
    if not execution_id:
        raise ValueError("execution_id is required")

    safe_operation_id = re.sub(r"[^A-Za-z0-9._-]+", "-", operation_id).strip("-")
    safe_execution_id = re.sub(r"[^A-Za-z0-9._-]+", "-", execution_id).strip("-")
    if not safe_operation_id:
        raise ValueError("operation_id has no usable branch characters")
    if not safe_execution_id:
        raise ValueError("execution_id has no usable branch characters")

    return f"operation/{safe_operation_id}/{safe_execution_id}"


def execution_artifact(operation_id: str, execution_id: str) -> str:
    """Return a unique observation Artifact path for one execution instance."""
    branch = execution_branch(operation_id, execution_id)
    _, safe_operation_id, safe_execution_id = branch.split("/", 2)
    return f"docs/observations/{safe_operation_id}-operation-execution-{safe_execution_id}.md"
