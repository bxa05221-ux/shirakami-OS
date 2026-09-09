from runtime.operation_replay import execution_artifact, execution_branch
from runtime.operation_result import OperationResult


def test_result_identity_matches_replay_identity_inputs():
    result = OperationResult("R0077", "exec-001", "verified")

    assert result.identity == ("R0077", "exec-001")
    assert "R0077" in execution_branch(*result.identity)
    assert "exec-001" in execution_branch(*result.identity)
    assert "R0077" in execution_artifact(*result.identity)
    assert "exec-001" in execution_artifact(*result.identity)


def test_replayed_results_have_distinct_runtime_addresses():
    first = OperationResult("R0077", "exec-001", "verified")
    second = OperationResult("R0077", "exec-002", "verified")

    assert first.identity != second.identity
    assert execution_branch(*first.identity) != execution_branch(*second.identity)
    assert execution_artifact(*first.identity) != execution_artifact(*second.identity)


def test_outcome_does_not_change_execution_address():
    verified = OperationResult("R0077", "exec-001", "verified")
    observed = OperationResult("R0077", "exec-001", "observed")

    assert verified.identity == observed.identity
    assert execution_branch(*verified.identity) == execution_branch(*observed.identity)
    assert execution_artifact(*verified.identity) == execution_artifact(*observed.identity)
