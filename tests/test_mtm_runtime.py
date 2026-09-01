from runtime.mtm_compatibility import MTMProtocol
from runtime.mtm_runtime import RuntimeProtocol, prepare_runtime_protocol


def test_prepare_runtime_protocol_preserves_mtm_payload():
    source = {
        "protocol_id": "tsugaru-guide-highschool",
        "version": "0.1",
        "purpose": {"goal": "observe"},
        "future_field": {"preserve": True},
    }
    mtm = MTMProtocol(source_format="mapping", payload=source)

    runtime_protocol = prepare_runtime_protocol(mtm)

    assert isinstance(runtime_protocol, RuntimeProtocol)
    assert runtime_protocol.protocol_id == "tsugaru-guide-highschool"
    assert runtime_protocol.version == "0.1"
    assert dict(runtime_protocol.payload) == source


def test_prepare_runtime_protocol_accepts_existing_protocol_representation():
    source = {
        "protocol_id": "example.protocol",
        "version": "0.1",
        "statement": "Observe before acting.",
    }

    runtime_protocol = prepare_runtime_protocol(source)

    assert runtime_protocol.protocol_id == "example.protocol"
    assert runtime_protocol.version == "0.1"
    assert dict(runtime_protocol.payload) == source


def test_prepare_runtime_protocol_rejects_missing_identity():
    try:
        prepare_runtime_protocol({"version": "0.1"})
    except ValueError as exc:
        assert str(exc) == "MTM protocol requires protocol_id"
    else:
        raise AssertionError("protocol without protocol_id was accepted")
