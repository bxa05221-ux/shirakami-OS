"""API-level smoke tests: load -> register -> select -> invoke."""

from pathlib import Path

from runtime.protocol_api import build_protocol_request, invoke_protocol, register_temporary_matome
from runtime.protocol_loader import load_matome
from runtime.protocol_registry import ProtocolRegistry


ROOT = Path(__file__).resolve().parents[1]


def _artifact_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _smoke(path: Path, expected_id: str, expected_phases: list[str]) -> None:
    artifact = load_matome(path)
    assert artifact.protocol_id == expected_id
    assert [item["phase"] for item in artifact.pipeline] == expected_phases

    registry = ProtocolRegistry()
    entry = register_temporary_matome(registry, _artifact_text(path))
    assert entry.protocol_id == expected_id
    assert entry.state == "experimental"

    request = build_protocol_request(registry, expected_id, {"smoke": True})
    result = invoke_protocol(request, lambda req: {
        "protocol_id": req.protocol_id,
        "version": req.version,
        "input": dict(req.input),
    })
    assert result["protocol_id"] == expected_id
    assert result["input"] == {"smoke": True}


def test_3d_pruim_registry_api_smoke():
    _smoke(
        ROOT / "protocols/language/3d-pruim.yaml",
        "3d.phase.rotational.urgency.importance.matrix",
        ["phase_rotation", "vector_decomposition", "quadrant_classification", "small_step_generation"],
    )


def test_anmon_registry_api_smoke():
    _smoke(
        ROOT / "protocols/language/anmon-layer-reverse.yaml",
        "protocol",
        ["surface_capture", "layer_stripping", "b_side_extraction", "resonance_lock", "reverse_engineering", "consistency_check"],
    )
