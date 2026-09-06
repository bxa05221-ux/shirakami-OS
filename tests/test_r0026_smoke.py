def test_r0026_smoke():
    from runtime.landscape import LandscapeState
    from runtime.landscape_execution import execute_on_landscape
    from runtime.prototype import Transition

    state = LandscapeState.from_snapshot({"branch": "main"})

    def protocol(context):
        return Transition(kind="r0026.transition", data={"branch": "r0026", "changed": True})

    result = execute_on_landscape(state, "r0026.protocol", protocol)
    assert result.status == "completed"
    assert state.snapshot()["branch"] == "r0026"
    assert len(state.evidence) == 1
