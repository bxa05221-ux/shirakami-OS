from runtime.trace import ExecutionTrace, ExecutionTraceStore


def _trace():
    return ExecutionTrace(
        trace_id="TRACE-001",
        execution_id="EXEC-001",
        handoff_id="SH-HO-20260925-001",
        evidence_ids=("EVIDENCE-001",),
        project="Shirakami Project",
        objective="API provenance",
        protocol_ids=("api.example",),
        verification_scope=("runtime handle",),
    )


def test_execution_trace_preserves_provenance_without_authority():
    trace = _trace()
    assert trace.execution_id == "EXEC-001"
    assert trace.handoff_id == "SH-HO-20260925-001"
    assert trace.evidence_ids == ("EVIDENCE-001",)
    assert trace.verification_status == "pending"
    assert trace.execution_authorized is False
    assert trace.publish_authorized is False
    assert trace.merge_authorized is False
    assert trace.human_gate_required is True


def test_trace_rejects_authority():
    try:
        ExecutionTrace(
            **{**_trace().__dict__, "execution_authorized": True}
        )
    except ValueError as exc:
        assert "authority" in str(exc)
    else:
        raise AssertionError("authority must be rejected")


def test_verification_creates_new_immutable_trace_revision():
    store = ExecutionTraceStore()
    original = store.create(_trace())
    updated = store.attach_verification(
        "TRACE-001",
        status="pass",
        uncertainty="low",
        observed={"transition_kind": "api.example"},
    )

    assert updated is not None
    assert original.verification_status == "pending"
    assert updated.verification_status == "pass"
    assert updated.verification_observed == {"transition_kind": "api.example"}
    assert store.get("TRACE-001") == updated


def test_unknown_trace_fails_closed():
    store = ExecutionTraceStore()
    assert store.attach_verification(
        "missing",
        status="pass",
        uncertainty="low",
        observed={},
    ) is None
