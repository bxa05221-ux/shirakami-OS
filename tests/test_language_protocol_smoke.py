"""Smoke tests for language protocols that can be loaded without new Runtime semantics."""

from pathlib import Path

from runtime.protocol_loader import load_matome


ROOT = Path(__file__).resolve().parents[1]


def test_3d_pruim_loads_as_protocol_ir():
    protocol = load_matome(ROOT / "protocols/language/3d-pruim.yaml")
    assert protocol.title == "3D Phase Rotational Urgency-Importance Matrix"
    assert protocol.version == "0.1"
    assert [item["phase"] for item in protocol.pipeline] == [
        "phase_rotation",
        "vector_decomposition",
        "quadrant_classification",
        "small_step_generation",
    ]


def test_anmon_layer_reverse_loads_as_protocol_ir():
    protocol = load_matome(ROOT / "protocols/language/anmon-layer-reverse.yaml")
    assert protocol.title == "暗問層逆算プロトコル"
    assert protocol.version == "0.1"
    assert [item["phase"] for item in protocol.pipeline] == [
        "surface_capture",
        "layer_stripping",
        "b_side_extraction",
        "resonance_lock",
        "reverse_engineering",
        "consistency_check",
    ]
