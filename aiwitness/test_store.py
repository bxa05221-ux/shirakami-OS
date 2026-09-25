from aiwitness.store import WitnessStore
from aiwitness.witness import AIwitness
from runtime.trace import ExecutionTrace


def make_trace() -> ExecutionTrace:
    return ExecutionTrace(
        trace_id="TRACE-STORE-001",
        execution_id="EXEC-STORE-001",
        handoff_id="SH-HO-20260925-001",
        evidence_ids=("EVID-STORE-001",),
        project="Shirakami",
        objective="store witness",
        protocol_ids=("P-STORE-001",),
        verification_scope=("test",),
        verification_status="pass",
        verification_observed={"test": "passed"},
    )


def test_witness_store_is_append_only_and_trace_addressable():
    store = WitnessStore()
    witness = AIwitness.observe(make_trace())

    assert store.record(witness) is witness
    assert store.get(witness.trace_id) == witness
    assert store.all() == (witness,)


def test_witness_store_does_not_change_authority():
    store = WitnessStore()
    witness = store.record(AIwitness.observe(make_trace()))

    assert witness.execution_authorized is False
    assert witness.publish_authorized is False
    assert witness.merge_authorized is False
    assert witness.human_gate_required is True
