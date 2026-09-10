"""Smoke test for directly adopting Thread RPG 3.2 as a language protocol."""

from pathlib import Path

from runtime.protocol_api import build_protocol_request, invoke_protocol, register_temporary_matome
from runtime.protocol_loader import load_matome
from runtime.protocol_registry import ProtocolRegistry


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "protocols/language/thread-rpg-v3.2.yaml"


def test_thread_rpg_v32_load_register_invoke():
    artifact = load_matome(PATH)
    assert artifact.protocol_id
    assert artifact.version == "3.2"
    assert [item["phase"] for item in artifact.pipeline] == [
        "observation",
        "response",
        "reaction",
        "correction_or_alignment",
        "unresolved_or_temporary_landing",
    ]

    registry = ProtocolRegistry()
    entry = register_temporary_matome(registry, PATH.read_text(encoding="utf-8"))
    assert entry.protocol_id == artifact.protocol_id
    assert entry.state == "experimental"

    request = build_protocol_request(registry, artifact.protocol_id, {"theme": "smoke"})
    result = invoke_protocol(request, lambda req: {
        "protocol_id": req.protocol_id,
        "version": req.version,
        "input": dict(req.input),
    })
    assert result["protocol_id"] == artifact.protocol_id
    assert result["version"] == "3.2"
    assert result["input"] == {"theme": "smoke"}
