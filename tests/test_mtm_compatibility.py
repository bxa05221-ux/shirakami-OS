from runtime.mtm_compatibility import MTMProtocol, normalize_protocol
from runtime.protocol_loader import ProtocolIR


def test_normalize_matome_ir_preserves_semantic_payload():
    protocol = ProtocolIR(
        protocol_id="example.protocol",
        title="Example Protocol",
        version="0.1",
        statement="Observe before acting.",
        pipeline=({"phase": "observe", "action": "record"},),
    )

    normalized = normalize_protocol(protocol)

    assert isinstance(normalized, MTMProtocol)
    assert normalized.source_format == "matome-ir"
    assert normalized.payload["protocol_id"] == protocol.protocol_id
    assert normalized.payload["title"] == protocol.title
    assert normalized.payload["version"] == protocol.version
    assert normalized.payload["statement"] == protocol.statement
    assert normalized.payload["pipeline"] == protocol.pipeline


def test_normalize_mapping_keeps_unknown_fields():
    source = {
        "protocol_id": "example.protocol",
        "version": "0.2",
        "purpose": {"goal": "observe"},
        "future_field": {"preserve": True},
    }

    normalized = normalize_protocol(source)

    assert normalized.source_format == "mapping"
    assert dict(normalized.payload) == source
    assert normalized.payload["future_field"] == {"preserve": True}


def test_normalize_rejects_unsupported_representation():
    try:
        normalize_protocol(object())
    except TypeError as exc:
        assert str(exc) == "unsupported protocol representation"
    else:
        raise AssertionError("unsupported representation was accepted")
