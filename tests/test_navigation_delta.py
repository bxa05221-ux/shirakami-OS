from runtime.navigation_delta import NavigationBeacon, NavigationDelta


def test_beacon_is_immutable_and_contains_only_observations():
    beacon = NavigationBeacon(
        position="A",
        direction="north",
        attitude="level",
        horizon=["B"],
        uncertainty=("unknown-distance",),
        evidence_cursor=("p1", "changed"),
        landscape_changed=True,
    )

    assert beacon.snapshot()["position"] == "A"
    assert beacon.snapshot()["direction"] == "north"
    assert "destination" not in beacon.snapshot()
    assert "course" not in beacon.snapshot()


def test_delta_reports_observable_changes_only():
    before = {
        "position": "A",
        "direction": "north",
        "attitude": "level",
        "horizon": ["B"],
        "landscape_revision": 1,
        "evidence_cursor": ("p1", "changed"),
        "uncertainty": [],
    }
    after = {
        **before,
        "position": "A2",
        "direction": "northeast",
        "landscape_revision": 2,
        "evidence_cursor": ("p2", "changed"),
    }

    delta = NavigationDelta.between(before, after)

    assert delta.changed is True
    assert delta.changed_fields == (
        "position",
        "direction",
        "landscape_revision",
        "evidence_cursor",
    )


def test_delta_can_be_unchanged():
    state = {"position": "A", "direction": "north"}
    delta = NavigationDelta.between(state, state, fields=("position", "direction"))

    assert delta.changed is False
    assert delta.changed_fields == ()
