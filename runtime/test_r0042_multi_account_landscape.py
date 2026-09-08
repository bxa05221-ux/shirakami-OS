from evidence import capture_evidence
from landscape_adapter import InMemoryLandscapeAdapter
from prototype import Runtime, example_protocol


def test_multi_account_landscape_preserves_account_provenance():
    result_a = Runtime().execute(
        "example.protocol",
        example_protocol,
        {"message": "account-a"},
    )
    evidence_a = capture_evidence(result_a)

    result_b = Runtime().execute(
        "example.protocol",
        example_protocol,
        {"message": "account-b"},
    )
    evidence_b = capture_evidence(result_b)

    adapter_a = InMemoryLandscapeAdapter()
    adapter_b = InMemoryLandscapeAdapter()
    adapter_a.apply_transition(evidence_a)
    adapter_b.apply_transition(evidence_b)

    shared_landscape = {
        "account_a": adapter_a.read_state(),
        "account_b": adapter_b.read_state(),
    }

    assert shared_landscape["account_a"] == adapter_a.read_state()
    assert shared_landscape["account_b"] == adapter_b.read_state()
    assert evidence_a.protocol_id == "example.protocol"
    assert evidence_b.protocol_id == "example.protocol"
    assert evidence_a is not evidence_b


def test_multi_account_landscape_does_not_merge_account_states():
    adapter_a = InMemoryLandscapeAdapter({"account": "a", "value": 1})
    adapter_b = InMemoryLandscapeAdapter({"account": "b", "value": 2})

    shared_landscape = {
        "account_a": adapter_a.read_state(),
        "account_b": adapter_b.read_state(),
    }

    assert shared_landscape["account_a"] == {"account": "a", "value": 1}
    assert shared_landscape["account_b"] == {"account": "b", "value": 2}
    assert shared_landscape["account_a"] != shared_landscape["account_b"]
