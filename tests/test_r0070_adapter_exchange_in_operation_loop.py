from runtime.adapter import MemoryAdapter, adapt_landscape_observation
from runtime.landscape import LandscapeState
from runtime.observable_execution import execute_observably
from runtime.prototype import Runtime, example_protocol


def test_r0070_adapter_exchange_preserves_continuous_landscape_observation():
    adapter_a = MemoryAdapter(
        {"landscape": {"repository": "bxa05221-ux/shirakami-OS", "branch": "main"}}
    )
    adapter_b = MemoryAdapter(
        {"landscape": {"repository": "bxa05221-ux/shirakami-OS", "branch": "main"}}
    )

    state = LandscapeState.from_snapshot(adapter_a.read("landscape"))
    first = execute_observably(
        state, Runtime(), "example.protocol", example_protocol, {"message": "r0070-first"}
    )

    state_before_exchange = state.snapshot()
    evidence_before_exchange = tuple(state.evidence)
    exchanged_input = adapter_b.read("landscape")

    assert exchanged_input == adapter_a.read("landscape")
    assert state.snapshot() == state_before_exchange
    assert tuple(state.evidence) == evidence_before_exchange

    second = execute_observably(
        state, Runtime(), "example.protocol", example_protocol, {"message": "r0070-second"}
    )
    observation = adapt_landscape_observation(state)

    assert second.before_state == first.after_state
    assert observation["snapshot"] == second.after_state
    assert len(observation["evidence_lineage"]) == 2
    assert [item["protocol_id"] for item in observation["evidence_lineage"]] == [
        "example.protocol",
        "example.protocol",
    ]
    assert state.evidence == [first.evidence, second.evidence]
