from runtime.evidence import EvidenceRecord
from runtime.landscape import LandscapeState


def _evidence(protocol_id: str, value: str) -> EvidenceRecord:
    return EvidenceRecord(
        protocol_id=protocol_id,
        status="completed",
        transition_kind="update",
        transition_data={"changed": True, "value": value},
        signals=(f"signal-{value}",),
    )


def test_r0054_temporal_evidence_records_are_individually_addressable():
    state = LandscapeState.empty()
    evidence_a = _evidence("protocol.a", "A")
    evidence_b = _evidence("protocol.b", "B")
    evidence_c = _evidence("protocol.c", "C")

    state.apply_evidence(evidence_a)
    state.apply_evidence(evidence_b)
    state.apply_evidence(evidence_c)

    assert len(state.evidence) == 3
    assert state.evidence[0] is evidence_a
    assert state.evidence[1] is evidence_b
    assert state.evidence[2] is evidence_c

    assert state.evidence[0].protocol_id == "protocol.a"
    assert state.evidence[0].transition_data["value"] == "A"
    assert state.evidence[1].protocol_id == "protocol.b"
    assert state.evidence[1].transition_data["value"] == "B"
    assert state.evidence[2].protocol_id == "protocol.c"
    assert state.evidence[2].transition_data["value"] == "C"

    assert [record.protocol_id for record in state.evidence] == [
        "protocol.a",
        "protocol.b",
        "protocol.c",
    ]
