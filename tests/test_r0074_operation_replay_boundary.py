import pytest

from runtime.operation_replay import execution_artifact, execution_branch


def test_r0074_same_operation_gets_distinct_execution_branch():
    first = execution_branch("R0074", "1001")
    second = execution_branch("R0074", "1002")

    assert first == "operation/R0074/1001"
    assert second == "operation/R0074/1002"
    assert first != second


def test_r0074_same_operation_gets_distinct_artifact():
    first = execution_artifact("R0074", "1001")
    second = execution_artifact("R0074", "1002")

    assert first != second
    assert first.endswith("R0074-operation-execution-1001.md")
    assert second.endswith("R0074-operation-execution-1002.md")


def test_r0074_operation_id_is_safely_normalized():
    assert execution_branch("R/0074 test", "run:1") == "operation/R-0074-test/run-1"


def test_r0074_missing_execution_identity_is_rejected():
    with pytest.raises(ValueError, match="execution_id is required"):
        execution_branch("R0074", "")
