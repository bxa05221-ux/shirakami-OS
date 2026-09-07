from runtime.landscape import LandscapeState
from runtime.way import SmallStep
from runtime.wayfinding_cycle import execute_small_step


class Selector:
    def select(self, landscape):
        return SmallStep(action="write one sentence", reason="take one observable step")


class Applier:
    def apply(self, state, step):
        state._state["last_action"] = step.action


class Observer:
    def observe(self, state):
        return state.snapshot()


def test_wayfinding_cycle_observes_before_and_after_one_step():
    state = LandscapeState.from_snapshot({"place": "start"})
    cycle = execute_small_step(state, Selector(), Applier(), Observer())

    assert cycle.before == {"place": "start"}
    assert cycle.step.action == "write one sentence"
    assert cycle.after == {"place": "start", "last_action": "write one sentence"}


def test_wayfinding_cycle_keeps_selector_external():
    state = LandscapeState.from_snapshot({"place": "start"})
    cycle = execute_small_step(state, Selector(), Applier(), Observer())

    assert cycle.step.reason == "take one observable step"
