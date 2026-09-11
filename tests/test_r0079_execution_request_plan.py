import pytest

from runtime.execution_planner import plan_execution_request
from runtime.execution_request import ExecutionRequest
from runtime.operation_runner import OperationDefinition


def test_request_connects_to_existing_operation_plan():
    operation = OperationDefinition("R0079", "main", "implementation/operation")
    request = ExecutionRequest("R0079", "exec-001")

    plan = plan_execution_request(request, operation)

    assert plan.operation_id == "R0079"
    assert plan.base_ref == "main"
    assert plan.steps[-1] == "create-protected-pr"


def test_mismatched_operation_identity_is_rejected():
    operation = OperationDefinition("R0079", "main", "implementation/operation")
    request = ExecutionRequest("R9999", "exec-001")

    with pytest.raises(ValueError, match="does not match"):
        plan_execution_request(request, operation)


def test_request_planning_does_not_add_execution_authority():
    operation = OperationDefinition("R0079", "main", "implementation/operation")
    request = ExecutionRequest("R0079", "exec-001")

    plan_execution_request(request, operation)

    assert not hasattr(request, "execute")
