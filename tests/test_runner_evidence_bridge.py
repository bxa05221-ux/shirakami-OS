from runtime.background_runner_evidence import RunnerEvidence
from runtime.runner_evidence_bridge import (
    runner_evidence_batch_to_evidence,
    runner_evidence_to_evidence,
)


def test_runner_evidence_maps_to_canonical_evidence_without_authority():
    source = RunnerEvidence(
        event="verification_requested",
        protocol_identity="protocol-1",
        activation_identity="activation-1",
        approval_identity="reviewer-1",
        run_identity="run-1",
        iteration=2,
        runner_state="VERIFYING",
    )

    evidence = runner_evidence_to_evidence(source)

    assert evidence.protocol_id == "protocol-1"
    assert evidence.status == "observed"
    assert evidence.transition_kind == "runner:verification_requested"
    assert evidence.signals == ("runner:verification_requested",)
    assert evidence.transition_data["protocol_identity"] == "protocol-1"
    assert evidence.transition_data["activation_identity"] == "activation-1"
    assert evidence.transition_data["approval_identity"] == "reviewer-1"
    assert evidence.transition_data["run_identity"] == "run-1"
    assert evidence.transition_data["iteration"] == 2
    assert evidence.transition_data["runner_state"] == "VERIFYING"
    assert not hasattr(evidence, "authority")
    assert not hasattr(evidence, "execution_authorized")


def test_runner_stopped_mismatch_remains_observed_runner_state():
    source = RunnerEvidence(
        event="runner_stopped",
        protocol_identity="protocol-1",
        activation_identity="activation-1",
        approval_identity="reviewer-1",
        run_identity="run-1",
        iteration=2,
        runner_state="STOPPED",
    )

    evidence = runner_evidence_to_evidence(source)

    assert evidence.status == "observed"
    assert evidence.transition_kind == "runner:runner_stopped"
    assert evidence.transition_data["runner_state"] == "STOPPED"


def test_runner_evidence_batch_preserves_order_and_identity():
    source = (
        RunnerEvidence("runner_started", "p", "a", "r", "run", 0, "READY"),
        RunnerEvidence("iteration_started", "p", "a", "r", "run", 1, "RUNNING"),
    )

    evidence = runner_evidence_batch_to_evidence(source)

    assert tuple(item.transition_data["event"] for item in evidence) == (
        "runner_started",
        "iteration_started",
    )
    assert tuple(item.transition_data["run_identity"] for item in evidence) == (
        "run",
        "run",
    )
