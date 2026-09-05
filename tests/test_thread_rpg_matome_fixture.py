"""Verify Thread RPG can be represented by the β0.1 Matome input contract."""

from pathlib import Path

from runtime.protocol_loader import load_matome


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "thread-rpg-v1.2.1-matome.yaml"


def test_thread_rpg_matome_fixture_loads_into_protocol_ir():
    protocol = load_matome(FIXTURE)

    assert protocol.protocol_id == "thread.rpg.protocol"
    assert protocol.title == "Thread RPG Protocol"
    assert protocol.version == "1.2.1"
    assert protocol.statement
    assert len(protocol.pipeline) == 5
    assert protocol.pipeline[0]["phase"] == "multi_voice_dialogue"
    assert protocol.pipeline[-1]["phase"] == "human_readable_ai_behavior"
