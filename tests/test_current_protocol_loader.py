from pathlib import Path

from runtime.protocol_loader_v2 import parse_protocol


def test_current_tsugaru_guide_protocol_loads_as_current_protocol():
    text = Path("protocols/tsugaru-guide-highschool.yaml").read_text(encoding="utf-8")

    protocol = parse_protocol(text)

    assert protocol.protocol_id == "cheseborough-vr"
    assert protocol.version == "0.1"
    assert protocol.status == "experimental"
    assert protocol.purpose
    assert protocol.principles
    assert protocol.participants
    assert protocol.learning_cycle
    assert protocol.evidence
