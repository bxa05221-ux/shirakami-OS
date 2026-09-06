from runtime.evidence import EvidenceRecord
from runtime.evidence_delta import select_delta_evidence


def record(value: str) -> EvidenceRecord:
    return EvidenceRecord(
        protocol_id="example.protocol",
        status="success",
        transition_kind="example.transition",
        transition_data={"value": value, "changed": True},
        signals=(),
    )


def test_select_delta_evidence_preserves_order_and_input() -> None:
    one, two, three = record("one"), record("two"), record("three")
    source = [one, two, three]
    applied = [one, two]

    delta = select_delta_evidence(source, applied)

    assert delta == [three]
    assert source == [one, two, three]
    assert applied == [one, two]
