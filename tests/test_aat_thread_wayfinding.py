from dataclasses import dataclass

from runtime.aat_thread_wayfinding import run_aats_wayfinding
from runtime.aats import Participant, Post, Thread
from runtime.landscape import LandscapeState
from runtime.way import SmallStep


class Observer:
    def observe(self, state):
        return state.snapshot()


@dataclass
class Selector:
    def select(self, landscape):
        return SmallStep(action="take one small step", reason="continue from current observation")


class Applier:
    def apply(self, state, step):
        state._state["last_action"] = step.action


def test_aats_thread_completes_one_observe_step_reobserve_turn():
    thread = (
        Thread("thread-1")
        .with_participant(Participant("名無し001"))
        .with_participant(Participant("名無し002"))
        .with_post(Post("名無し001", "まず現在地を見よう", "( ˘ω˘ )"))
        .with_post(Post("名無し002", "でも一歩は進めたい"))
    )
    state = LandscapeState.from_snapshot({"location": "current"})

    result = run_aats_wayfinding(thread, state, Selector(), Applier(), Observer())

    assert [v.text for v in result.viewpoints] == ["まず現在地を見よう", "でも一歩は進めたい"]
    assert "名無し001" not in result.narrative
    assert result.before == {"location": "current"}
    assert result.small_step.action == "take one small step"
    assert result.after["last_action"] == "take one small step"
