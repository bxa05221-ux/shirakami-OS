from development_evidence import parse_development_evidence


def test_parse_development_evidence_is_deterministic_and_provenance_aware():
    text = '''# Development Evidence\n\n- Date: 2026-09-21\n- Protocol ID: R0100\n- Status: merged\n\n## Observation\n- Runtime boundary required an execution handle.\n\n## Change\n- Added observable lookup and handle verification.\n\n## Verification Evidence\n- CI workflow conclusion succeeded.\n\n## Boundary\n- Persistence remains in-memory.\n'''

    record = parse_development_evidence(text, source_ref="docs/evidence/example.md")

    assert record.evidence_id == "docs/evidence/example.md"
    assert record.observed_at == "2026-09-21"
    assert record.protocol_id == "R0100"
    assert record.status == "merged"
    assert record.claims == ("Runtime boundary required an execution handle.",)
    assert record.verification == ("CI workflow conclusion succeeded.",)
    assert record.limitations == ("Persistence remains in-memory.",)
    assert record.provenance["source_ref"] == "docs/evidence/example.md"
    assert record.as_dict()["provenance"] == {
        "parser": "alpha-0.1",
        "source_ref": "docs/evidence/example.md",
    }


def test_missing_values_are_explicit():
    record = parse_development_evidence("# Evidence\n", source_ref="x.md")

    assert record.protocol_id == "unknown"
    assert record.status == "unknown"
    assert record.summary == "unknown"
    assert record.human_gate == "unknown"
