from runtime.threadrpg_v4_hanaichimonme import Axis, Field, Resident, plan_reactions
import pytest


def test_seven_core_residents_and_reproducibility():
    first = plan_reactions("thread-1", 0)
    assert first == plan_reactions("thread-1", 0)
    assert len(first.residents) == 7
    assert len({r.participant_id for r in first.residents}) == 7


def test_axis_independence_and_dispersion():
    flat = plan_reactions("thread-1", 0, Field(content=Axis(12, 0)))
    assert {r.content for r in flat.residents} == {12}
    varied = plan_reactions("thread-1", 0, Field(content=Axis(50, 40)))
    assert all(10 <= r.content <= 90 for r in varied.residents)
    assert len({r.content for r in varied.residents}) > 1


def test_rom_does_not_become_core_member():
    field = plan_reactions("thread-1", 0, dormant=(Resident("comet-1", "work"),))
    assert len(field.residents) == 7
    assert all(r.participant_id != "comet-1" for r in field.residents)


@pytest.mark.parametrize("value", [-1, 101, True, 2.5])
def test_reject_invalid_axis(value):
    with pytest.raises(ValueError):
        Axis(center=value)


def test_reject_duplicate_rom():
    with pytest.raises(ValueError):
        plan_reactions("t", 0, dormant=(Resident("x", "a"), Resident("x", "b")))
