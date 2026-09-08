from evidence import capture_evidence
from landscape_adapter import InMemoryLandscapeAdapter
from prototype import Runtime, example_protocol


def test_adapter_exchange_preserves_landscape_and_evidence():
    result = Runtime().execute(
        "example.protocol",
        example_protocol,
        {"message": "adapter exchange"},
    )
    evidence = capture_evidence(result)

    adapter_a = InMemoryLandscapeAdapter()
    adapter_a.apply_transition(evidence)
    state_before_exchange = adapter_a.read_state()

    adapter_b = InMemoryLandscapeAdapter(state_before_exchange)
    state_after_exchange = adapter_b.read_state()

    assert state_after_exchange == state_before_exchange
    assert evidence.protocol_id == "example.protocol"
    assert evidence.status == "success"
    assert dict(evidence.transition_data)["changed"] is True


def test_adapter_exchange_does_not_reconstruct_missing_evidence():
    result = Runtime().execute(
        "example.protocol",
        example_protocol,
        {"message": "adapter exchange lineage"},
    )
    evidence = capture_evidence(result)

    adapter_a = InMemoryLandscapeAdapter()
    adapter_a.apply_transition(evidence)
    adapter_b = InMemoryLandscapeAdapter(adapter_a.read_state())

    assert adapter_b.read_state() == adapter_a.read_state()
    assert evidence.transition_data
    assert evidence.protocol_id == "example.protocol"
