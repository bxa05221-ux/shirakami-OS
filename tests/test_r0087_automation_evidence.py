from runtime.automation_evidence import capture_automation_evidence
from runtime.operation_automation import AutomationStepResult


def test_capture_automation_evidence_preserves_step_observation():
    results = (
        AutomationStepResult(step="record-baseline", outcome="ok"),
        AutomationStepResult(step="run-test-runtime", outcome="passed"),
    )

    evidence = capture_automation_evidence("op-1", results)

    assert len(evidence) == 2
    assert evidence[0].protocol_id == "op-1"
    assert evidence[0].status == "observed"
    assert evidence[0].transition_kind == "operation_automation_step"
    assert evidence[0].transition_data["step"] == "record-baseline"
    assert evidence[1].transition_data["outcome"] == "passed"


def test_capture_automation_evidence_returns_immutable_records():
    evidence = capture_automation_evidence(
        "op-2", (AutomationStepResult(step="verify", outcome="ok"),)
    )

    try:
        evidence[0].transition_data["step"] = "changed"
        changed = True
    except TypeError:
        changed = False

    assert changed is False
