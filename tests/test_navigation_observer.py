from types import MappingProxyType

from runtime.evidence import EvidenceRecord
from runtime.navigation import NavigationState
from runtime.navigation_observer import NavigationObserver


def make_evidence(data, *, changed=True):
    return EvidenceRecord(
        protocol_id="test.protocol",
        status="ok",
        transition_kind="landscape.changed" if changed else "landscape.observed",
        transition_data=MappingProxyType(dict(data)),
        signals=("observed",),
    )


def test_observer_copies_only_explicit_navigation_fields():
    state = NavigationState()
    observer = NavigationObserver(state)

    observer.observe(make_evidence({
        "changed": True,
        "position": {"x": 1},
        "direction": {"heading": 90},
        "attitude": {"pitch": 2},
        "horizon": ["north"],
        "uncertainty": ["low-confidence-position"],
        "destination": "forbidden-to-infer",
    }))

    assert state.position == {"x": 1}
    assert state.direction == {"heading": 90}
    assert state.attitude == {"pitch": 2}
    assert state.horizon == ["north"]
    assert state.uncertainty == ["low-confidence-position"]
    assert state.landscape_revision == 1
    assert state.snapshot()["reference_frame"] is None


def test_non_transition_evidence_does_not_advance_landscape_revision():
    state = NavigationState()
    observer = NavigationObserver(state)

    observer.observe(make_evidence({
        "changed": False,
        "position": {"x": 2},
    }, changed=False))

    assert state.position == {"x": 2}
    assert state.landscape_revision == 0


def test_observer_never_selects_reference_frame_or_destination():
    state = NavigationState()
    observer = NavigationObserver(state)

    observer.observe(make_evidence({
        "changed": True,
        "reference_frame": "should-not-be-selected",
        "destination": "should-not-be-selected",
    }))

    assert state.reference_frame is None
    assert state.position is None
    assert state.direction is None


def test_uncertainty_is_preserved_as_observation():
    state = NavigationState()
    observer = NavigationObserver(state)

    observer.observe(make_evidence({
        "changed": True,
        "uncertainty": ["direction-uncertain", "horizon-partial"],
    }))

    assert state.uncertainty == ["direction-uncertain", "horizon-partial"]
