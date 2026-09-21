from runtime.oppai_runtime_flow import discover_protocol_candidates
from runtime.protocol_loader import parse_matome
from runtime.protocol_registry import ProtocolRegistry


def _protocol(title: str, statement: str):
    return parse_matome(
        f"""matome:
  title: "{title}"
  version: "0.1"
  statement: >
    {statement}
  pipeline:
    - phase: observe
      action: inspect
"""
    )


def test_candidate_discovery_records_observable_lexical_basis_without_ranking():
    registry = ProtocolRegistry()
    registry.register_temporary(
        "writing",
        _protocol("文章作成", "文章を整理して編集する。"),
    )
    registry.register_temporary(
        "evidence",
        _protocol("証拠整理", "Evidenceを確認して整理する。"),
    )

    candidates = discover_protocol_candidates("文章を整理して", registry)

    writing = next(candidate for candidate in candidates if candidate.protocol_id == "writing")
    assert writing.basis == "observable.lexical_match"
    assert "文章" in writing.metadata["matched_terms"]
    assert [candidate.protocol_id for candidate in candidates] == ["writing", "evidence"]
