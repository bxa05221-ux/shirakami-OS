from runtime.mtm_compat import MTMProtocol, normalize
from runtime.protocol_loader import ProtocolIR


def test_normalize_preserves_existing_matome_ir():
    protocol = ProtocolIR(
        protocol_id="example.protocol",
        title="Example Protocol",
        version="0.1",
        statement="observe before acting",
        pipeline=({"phase": "observe", "action": "record"},),
    )

    normalized = normalize(protocol, source_format="matome-beta-0.1")

    assert isinstance(normalized, MTMProtocol)
    assert normalized.protocol_id == "example.protocol"
    assert normalized.version == "0.1"
    assert normalized.name == "Example Protocol"
    assert normalized.source_format == "matome-beta-0.1"
    assert normalized.payload["statement"] == "observe before acting"
    assert normalized.payload["pipeline"] == protocol.pipeline


def test_normalize_accepts_mapping_without_rewriting_payload():
    payload = {
        "protocol_id": "tsugaru-guide-highschool",
        "name": "TSUGARU GUIDE HIGH SCHOOL COLLABORATION PROTOCOL",
        "version": "0.1",
        "purpose": {"primary": "landscape"},
        "participants": {"students": {"role": "regional_observer"}},
    }

    normalized = normalize(payload, source_format="current-protocol")

    assert normalized.protocol_id == payload["protocol_id"]
    assert normalized.payload == payload
    assert normalized.payload["purpose"] == payload["purpose"]
    assert normalized.payload["participants"] == payload["participants"]
