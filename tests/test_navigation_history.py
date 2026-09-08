from runtime.navigation_history import NavigationHistory


def test_direction_trend_counts_observed_changes_only():
    history = NavigationHistory()
    history.record({"direction": "north"})
    history.record({"direction": "north"})
    history.record({"direction": "east"})
    history.record({"direction": "east"})

    trend = history.direction_trend()

    assert trend.samples == ("north", "north", "east", "east")
    assert trend.changed is True
    assert trend.change_count == 1


def test_empty_history_has_no_direction_change():
    trend = NavigationHistory().direction_trend()

    assert trend.samples == ()
    assert trend.changed is False
    assert trend.change_count == 0
