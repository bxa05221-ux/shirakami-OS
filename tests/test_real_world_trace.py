from examples.real_world_trace import run_example


def test_real_world_trace_is_reconstructable():
    result = run_example()

    assert result["routing"].selected_protocol == "cold-storage-check"
    assert result["simulation"].status == "completed"
    assert result["witness"].evidence_refs == (
        "TEMP-2026-09-19-001",
        "STOCK-2026-09-19-001",
    )
    assert result["decision"].status == "approved"
    assert result["operation"].status == "completed"
    assert result["operation"].reality_changed is False

    trace = result["trace"]
    assert trace.context_version == "demo-1.0"
    assert trace.input_evidence_refs == (
        "TEMP-2026-09-19-001",
        "STOCK-2026-09-19-001",
    )
    assert trace.resulting_evidence_refs == ("INSPECTION-2026-09-19-001",)
