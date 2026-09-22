from background_runner_evidence import RunnerEvidence
from evidence_store import EvidenceStore
from runner_evidence_store import append_runner_evidence


def _runner(event: str, iteration: int, state: str) -> RunnerEvidence:
    return RunnerEvidence(
        event=event,
        protocol_identity="protocol-1",
        activation_identity="activation-1",
        approval_identity="reviewer-1",
        run_identity="run-1",
        iteration=iteration,
        runner_state=state,
    )


def test_runner_evidence_is_stored_as_canonical_evidence():
    store = append_runner_evidence(
        EvidenceStore(),
        (
            _runner("runner_started", 0, "RUNNING"),
            _runner("runner_stopped", 1, "STOPPED"),
        ),
    )

    records = store.all()
    assert len(records) == 2
    assert [r.transition_kind for r in records] == [
        "runner:runner_started",
        "runner:runner_stopped",
    ]
    assert records[0].transition_data["approval_identity"] == "reviewer-1"
    assert records[1].transition_data["runner_state"] == "STOPPED"


def test_runner_evidence_store_bridge_preserves_order_and_does_not_mutate_source():
    source = EvidenceStore()
    evidence = (
        _runner("iteration_started", 1, "RUNNING"),
        _runner("verification_requested", 1, "VERIFYING"),
    )

    result = append_runner_evidence(source, evidence)

    assert source.all() == ()
    assert len(result.all()) == 2
    assert [r.transition_data["iteration"] for r in result.all()] == [1, 1]
    assert all(r.status == "observed" for r in result.all())


def test_runner_evidence_store_bridge_rejects_invalid_store():
    evidence = (_runner("runner_started", 0, "RUNNING"),)

    try:
        append_runner_evidence(None, evidence)  # type: ignore[arg-type]
    except TypeError as exc:
        assert str(exc) == "EvidenceStore is required"
    else:
        raise AssertionError("invalid store must fail closed")
