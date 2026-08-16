from prototype import ExecutionBudget, Runtime, example_protocol


def test_execution_budget_accepts_one_step_vertical_slice():
    result = Runtime(ExecutionBudget(max_steps=1)).execute("example.protocol", example_protocol, {})
    assert result.status == "completed"
    assert result.steps == 1


def test_execution_budget_rejects_invalid_limit_observably():
    result = Runtime(ExecutionBudget(max_steps=0)).execute("example.protocol", example_protocol, {})
    assert result.status == "failed"
    assert result.transition.kind == "execution.budget.invalid"


def test_execution_budget_does_not_change_protocol_semantics():
    result = Runtime(ExecutionBudget(max_steps=1)).execute("example.protocol", example_protocol, {"x": 1})
    assert result.transition.kind == "example.transition"
    assert result.transition.data["input"] == {"x": 1}
