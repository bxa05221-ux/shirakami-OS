from runtime.prototype import Transition
from shirakami_os import ShirakamiOS


def message_protocol(context):
    return Transition(
        kind="landscape.message.received",
        data={"changed": True, "message": context.input.get("message", "")},
    )


def test_each_os_instance_has_an_isolated_landscape():
    user_a = ShirakamiOS()
    user_b = ShirakamiOS()

    user_a.boot({"user": "A", "state": "ready"})
    user_b.boot({"user": "B", "state": "ready"})

    assert user_a.landscape.snapshot() == {"user": "A", "state": "ready"}
    assert user_b.landscape.snapshot() == {"user": "B", "state": "ready"}
    assert user_a.landscape is not user_b.landscape


def test_landscape_changes_do_not_cross_workspace_boundary():
    user_a = ShirakamiOS()
    user_b = ShirakamiOS()

    user_a.boot({"user": "A", "state": "ready"})
    user_b.boot({"user": "B", "state": "ready"})

    user_a.execute(
        "example.landscape.message",
        message_protocol,
        {"message": "only A"},
    )

    assert user_a.landscape.snapshot()["message"] == "only A"
    assert "message" not in user_b.landscape.snapshot()
