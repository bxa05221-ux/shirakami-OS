from runtime.navigation import NavigationState
from runtime.navigation_simulation import NavigationSimulator


def test_projection_preserves_observed_state_and_marks_condition() -> None:
    state = NavigationState(position="P0", direction="east", landscape_revision=3)

    scenarios = NavigationSimulator().project(state, steps=3)

    assert [s.step for s in scenarios] == [1, 2, 3]
    assert all(s.state["position"] == "P0" for s in scenarios)
    assert all(s.state["direction"] == "east" for s in scenarios)
    assert all(s.state["projection"] == "conditional" for s in scenarios)
    assert all(s.state["basis"] == "continue_observed_direction" for s in scenarios)


def test_projection_rejects_invalid_step_count() -> None:
    state = NavigationState()
    simulator = NavigationSimulator()

    for steps in (0, -1, 1.5):
        try:
            simulator.project(state, steps=steps)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid steps must be rejected")
