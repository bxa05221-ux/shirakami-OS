import pytest

from runtime.navigation_scenario import NavigationScenario


def test_scenario_repeats_latest_observed_state_and_marks_projection():
    snapshot = {
        "position": "P2",
        "direction": "east",
        "horizon": ["H1"],
        "uncertainty": ["U1"],
    }

    scenario = NavigationScenario.continue_observed_state(snapshot, steps=3)

    assert scenario.assumption == "continue_latest_observed_state"
    assert len(scenario.steps) == 3
    assert scenario.steps[0]["position"] == "P2"
    assert scenario.steps[2]["direction"] == "east"
    assert all(step["synthetic"] is True for step in scenario.steps)
    assert all(step["projection_step"] == i for i, step in enumerate(scenario.steps, 1))


def test_scenario_requires_positive_steps():
    with pytest.raises(ValueError):
        NavigationScenario.continue_observed_state({}, steps=0)
