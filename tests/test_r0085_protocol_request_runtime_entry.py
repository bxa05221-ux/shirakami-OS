from runtime.protocol_api import ProtocolRequest, ProtocolAPIError
from runtime.protocol_request_runtime_entry import execute_protocol_request


def test_protocol_request_is_passed_to_existing_executor():
    request = ProtocolRequest(protocol_id="r0085-test", version="1", input={"value": "ok"})
    seen = {}

    def executor(received):
        seen["request"] = received
        return {"status": "executed", "protocol_id": received.protocol_id}

    result = execute_protocol_request(request, executor)

    assert seen["request"] is request
    assert result == {"status": "executed", "protocol_id": "r0085-test"}


def test_protocol_request_entry_rejects_missing_request():
    try:
        execute_protocol_request(None, lambda request: request)
    except ProtocolAPIError as exc:
        assert str(exc) == "ProtocolRequest is required"
    else:
        raise AssertionError("expected ProtocolAPIError")


def test_protocol_request_entry_rejects_missing_executor():
    request = ProtocolRequest(protocol_id="r0085-test", version=None, input={})
    try:
        execute_protocol_request(request, None)
    except ProtocolAPIError as exc:
        assert str(exc) == "executor is required"
    else:
        raise AssertionError("expected ProtocolAPIError")
