from api.runtime_api import execute


def test_api_execute_echo():
    response = execute(
        {
            "protocol": {"matome": {"title": "API Test", "version": "0.1"}},
            "operation": "echo",
            "input": {"landscape": "test"},
        }
    )

    assert response["protocol"]["title"] == "API Test"
    assert response["protocol"]["version"] == "0.1"
    assert response["success"] is True
    assert response["event"] == "execution.completed"
    assert response["output"] == {"landscape": "test"}


def test_api_rejects_unknown_operation():
    try:
        execute({"protocol": {"matome": {}}, "operation": "unknown"})
    except ValueError as exc:
        assert str(exc) == "unsupported operation"
    else:
        raise AssertionError("expected ValueError")
