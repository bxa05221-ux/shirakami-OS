from evolution_loop import EvidenceClass, EvolutionLoop, LoopState


def test_normal_loop_reaches_accepted():
    loop = EvolutionLoop()
    for event in ("observe", "evidence", "analyze", "existing_protocol", "execute", "verify", "pass"):
        result = loop.dispatch(event)
        assert result.accepted is True
    assert loop.state is LoopState.ACCEPTED


def test_unknown_transition_fails_closed_and_becomes_failure_evidence():
    loop = EvolutionLoop()
    result = loop.dispatch("execute")
    assert result.accepted is False
    assert loop.state is LoopState.IDLE
    assert loop.records[-1].evidence_class is EvidenceClass.FAILURE
    assert loop.evidence[-1].source == "transition_record"


def test_human_gate_blocks_without_approval():
    loop = EvolutionLoop()
    for event in ("observe", "evidence", "analyze", "new_protocol", "review"):
        assert loop.dispatch(event).accepted
    result = loop.dispatch("approve")
    assert result.accepted is False
    assert loop.state is LoopState.HUMAN_REVIEW
    assert loop.records[-1].evidence_class is EvidenceClass.FAILURE

    result = loop.dispatch("approve", human_approved=True)
    assert result.accepted is True
    assert loop.state is LoopState.READY
    assert loop.evidence[-1].evidence_class is EvidenceClass.HUMAN_DECISION


def test_mismatch_becomes_evidence_and_can_reenter_protocol_candidate():
    loop = EvolutionLoop()
    for event in ("observe", "evidence", "analyze", "existing_protocol", "execute", "verify"):
        assert loop.dispatch(event).accepted
    assert loop.dispatch("mismatch").accepted
    assert loop.evidence[-1].evidence_class is EvidenceClass.MISMATCH
    assert loop.dispatch("protocol_change").accepted
    assert loop.state is LoopState.PROTOCOL_CANDIDATE
