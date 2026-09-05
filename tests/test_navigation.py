from runtime.navigation import AUTOPILOT_FORBIDDEN_OPERATIONS, NavigationState


def test_navigation_starts_without_assumed_position_or_reference():
    state = NavigationState()
    snapshot = state.snapshot()

    assert snapshot["position"] is None
    assert snapshot["direction"] is None
    assert snapshot["reference_frame"] is None
    assert snapshot["map_id"] == "distorted_celestial_sphere"


def test_navigation_observation_updates_position_direction_and_landscape_revision():
    state = NavigationState()

    state.observe(
        position="landscape:current",
        direction="north-east",
        attitude="stable",
        horizon="far-field",
        evidence_cursor="evidence:001",
        landscape_changed=True,
        uncertainty=["direction approximate"],
    )

    snapshot = state.snapshot()
    assert snapshot["position"] == "landscape:current"
    assert snapshot["direction"] == "north-east"
    assert snapshot["attitude"] == "stable"
    assert snapshot["horizon"] == "far-field"
    assert snapshot["evidence_cursor"] == "evidence:001"
    assert snapshot["landscape_revision"] == 1
    assert snapshot["uncertainty"] == ["direction approximate"]


def test_reference_frame_is_explicitly_selected():
    state = NavigationState()

    state.set_reference_frame("Christianity")

    assert state.snapshot()["reference_frame"] == "Christianity"


def test_empty_reference_frame_is_rejected():
    state = NavigationState()

    try:
        state.set_reference_frame(" ")
    except ValueError as exc:
        assert "reference_id" in str(exc)
    else:
        raise AssertionError("empty reference frame must be rejected")


def test_autopilot_operations_are_forbidden_by_contract():
    assert "choose_destination" in AUTOPILOT_FORBIDDEN_OPERATIONS
    assert "choose_values" in AUTOPILOT_FORBIDDEN_OPERATIONS
    assert "choose_faith" in AUTOPILOT_FORBIDDEN_OPERATIONS
    assert "change_course" in AUTOPILOT_FORBIDDEN_OPERATIONS
    assert "make_final_decision" in AUTOPILOT_FORBIDDEN_OPERATIONS
