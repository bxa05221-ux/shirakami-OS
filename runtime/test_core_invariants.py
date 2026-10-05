from dataclasses import FrozenInstanceError

from evolution_bridge import ContextSnapshot


def test_context_snapshot_does_not_grant_authority():
    snapshot = ContextSnapshot(
        landscape={"place": "test"},
        protocol_id="P001",
        runtime_state="READY",
        metadata={
            "authority_granted": True,
            "decision_authorized": True,
            "human_gate_required": True,
        },
    )

    mapping = snapshot.as_mapping()

    # Context records state; it must not manufacture authority.
    assert "authority_granted" not in mapping
    assert "decision_authorized" not in mapping
    assert mapping["metadata"]["human_gate_required"] is True


def test_context_snapshot_has_no_authority_attributes():
    snapshot = ContextSnapshot(
        landscape={"place": "test"},
        protocol_id="P001",
        runtime_state="READY",
        metadata={"authority_granted": True},
    )

    assert not hasattr(snapshot, "authority_granted")
    assert not hasattr(snapshot, "decision_authorized")


def test_context_snapshot_is_immutable():
    snapshot = ContextSnapshot(
        landscape={"place": "test"},
        protocol_id="P001",
        runtime_state="READY",
    )

    try:
        snapshot.runtime_state = "AUTHORIZED"
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("ContextSnapshot must remain immutable")
