import pytest

from runtime.operation_result import OperationResult


def test_result_identity_separates_operation_and_execution() -> None:
    result = OperationResult("R0075", "exec-001", "success")
    assert result.identity == ("R0075", "exec-001")
    assert result.outcome == "success"


def test_same_operation_different_executions_are_distinct() -> None:
    first = OperationResult("R0075", "exec-001", "success")
    second = OperationResult("R0075", "exec-002", "failure")
    assert first.identity != second.identity


@pytest.mark.parametrize("field", ["operation_id", "execution_id", "outcome"])
def test_missing_result_identity_is_rejected(field: str) -> None:
    values = {
        "operation_id": "R0075",
        "execution_id": "exec-001",
        "outcome": "success",
    }
    values[field] = ""
    with pytest.raises(ValueError):
        OperationResult(**values)
