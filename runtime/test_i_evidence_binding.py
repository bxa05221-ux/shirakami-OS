from evidence import EvidenceRecord
from evidence_identity import evidence_id, matches_evidence_ref
from i_field import IField, ImaginaryTerm


def test_i_resolution_can_be_bound_to_actual_evidence_identity():
    evidence = EvidenceRecord(
        protocol_id="example.protocol",
        status="success",
        transition_kind="state_update",
        transition_data={"changed": True, "message": "observed"},
        signals=("observed",),
    )
    ref = evidence_id(evidence)
    field = IField((ImaginaryTerm("i1", "left", "unresolved"),))

    assert matches_evidence_ref(evidence, ref)
    resolved = field.resolve("i1", "observed value", ref)

    assert resolved.evidence_ref == ref
    assert field.is_resolved()
