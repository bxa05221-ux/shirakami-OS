from runtime.landscape import LandscapeState
from runtime.landscape_execution import execute_on_landscape
from runtime.prototype import Transition


def update_protocol(context):
    return Transition(
        kind="r0026.landscape.update",
        data={
            "repository": context.input["repository"],
            "branch": context.input["branch"],
            "changed": True,
        },
    )


def test_external_landscape_can_enter_runtime_execution_and_return_as_evidence():
    state = LandscapeState.from_snapshot(
        {"repository": "bxa05221-ux/shirakami-OS", "branch": "main"}
    )

    result = execute_on_landscape(
        state,
        "r0026.test.protocol",
        update_protocol,
        {"repository": "bxa05221-ux/shirakami-OS", "branch": "r0026"},
    )

    assert result.status == "completed"
    assert len(state.evidence) == 1
    assert state.evidence[0].protocol_id == "r0026.test.protocol"
    assert state.snapshot()["branch"] == "r0026"
    assert state.snapshot()["repository"] == "bxa05221-ux/shirakami-OS"
