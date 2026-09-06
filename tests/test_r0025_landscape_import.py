from runtime.landscape import LandscapeState
from runtime.landscape_import import import_observation


def test_import_observation_preserves_snapshot_without_semantics():
    observation = {
        "snapshot": {"repository": "bxa05221-ux/shirakami-OS", "branch": "main"},
        "evidence_lineage": [],
    }

    state = import_observation(observation)

    assert isinstance(state, LandscapeState)
    assert state.snapshot() == observation["snapshot"]
    assert state.evidence == []


def test_import_observation_requires_snapshot_mapping():
    try:
        import_observation({"snapshot": None})
    except ValueError as exc:
        assert str(exc) == "observation.snapshot must be a mapping"
    else:
        raise AssertionError("expected ValueError")
