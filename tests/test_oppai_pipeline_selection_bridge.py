from runtime.oppai_runtime_flow import build_selected_protocol_request
from runtime.protocol_api import ProtocolRequest
from runtime.protocol_registry import ProtocolRegistry


def test_oppai_selected_protocol_uses_canonical_request_boundary():
    registry = ProtocolRegistry()
    registry.register(
        "oppai-selection-a",
        {"version": "0.1", "title": "Selection A"},
        state="experimental",
    )

    request = build_selected_protocol_request(
        "この件を整理したい",
        registry,
        selected_protocol="oppai-selection-a",
        context={"time": "now", "source": "human"},
    )

    assert isinstance(request, ProtocolRequest)
    assert request.protocol_id == "oppai-selection-a"
    assert request.version == "0.1"
    assert request.input["raw_input"] == "この件を整理したい"
    assert request.input["canonical_prompt"] == "この件を整理したい"
    assert request.input["context"]["source"] == "human"


def test_oppai_selected_protocol_does_not_silently_select():
    registry = ProtocolRegistry()
    registry.register(
        "oppai-selection-a",
        {"version": "0.1", "title": "Selection A"},
        state="experimental",
    )
    registry.register(
        "oppai-selection-b",
        {"version": "0.1", "title": "Selection B"},
        state="experimental",
    )

    request = build_selected_protocol_request(
        "別の処理をしたい",
        registry,
        selected_protocol="oppai-selection-b",
    )

    assert request.protocol_id == "oppai-selection-b"
    assert request.protocol_id != "oppai-selection-a"
