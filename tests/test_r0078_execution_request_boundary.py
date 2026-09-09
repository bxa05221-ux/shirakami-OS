from runtime.execution_request import ExecutionRequest


def test_request_identity_is_operation_and_execution_pair():
    request = ExecutionRequest("R0078", "exec-001")
    assert request.identity == ("R0078", "exec-001")


def test_same_operation_can_have_distinct_execution_requests():
    first = ExecutionRequest("R0078", "exec-001")
    second = ExecutionRequest("R0078", "exec-002")
    assert first.identity != second.identity


def test_execution_request_does_not_execute_operation():
    request = ExecutionRequest("R0078", "exec-001")
    assert not hasattr(request, "execute")


def test_missing_request_identity_is_rejected():
    for operation_id, execution_id in (("", "exec-001"), ("R0078", "")):
        try:
            ExecutionRequest(operation_id, execution_id)
        except ValueError:
            pass
        else:
            raise AssertionError("missing execution request identity must be rejected")
