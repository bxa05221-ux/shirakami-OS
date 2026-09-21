from runtime.oppai_runtime_flow import discover_protocol_candidates
from runtime.protocol_loader import parse_matome
from runtime.protocol_registry import ProtocolRegistry


def _protocol(title: str):
    return parse_matome(
        f"""matome:
  title: "{title}"
  version: "0.1"
  statement: >
    Test protocol.
  pipeline:
    - phase: observe
      action: inspect
"""
    )


def test_candidate_discovery_exposes_all_current_protocols_without_selection():
    registry = ProtocolRegistry()
    registry.register_temporary("alpha", _protocol("Alpha"))
    registry.register_temporary("beta", _protocol("Beta"))

    candidates = discover_protocol_candidates("整理して", registry)

    assert [candidate.protocol_id for candidate in candidates] == ["alpha", "beta"]
    assert all(candidate.basis == "registry.current" for candidate in candidates)
    assert all("state" in candidate.metadata for candidate in candidates)


def test_candidate_discovery_does_not_activate_a_protocol():
    registry = ProtocolRegistry()
    registry.register_temporary("alpha", _protocol("Alpha"))
    registry.register_temporary("beta", _protocol("Beta"))

    candidates = discover_protocol_candidates("betaっぽい依頼", registry)

    assert len(candidates) == 2
    assert [candidate.protocol_id for candidate in candidates] == ["alpha", "beta"]
    assert candidates[0].basis == "registry.current"
    assert candidates[1].basis == "observable.lexical_match"
    assert registry.snapshot()["alpha"].state == "experimental"
    assert registry.snapshot()["beta"].state == "experimental"
