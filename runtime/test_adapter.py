from adapter import MemoryAdapter
from prototype import Runtime, Transition


def test_adapter_is_replaceable_boundary():
    adapter = MemoryAdapter({"landscape:1": {"message": "from backend"}})
    record = adapter.read("landscape:1")

    runtime = Runtime()

    def protocol(context):
        return Transition(
            kind="adapter.transition",
            data={"message": context.input["message"]},
        )

    result = runtime.execute("adapter.protocol", protocol, record)

    assert result.status == "completed"
    assert result.transition.data["message"] == "from backend"


def test_adapter_missing_reference_remains_backend_error():
    adapter = MemoryAdapter()

    try:
        adapter.read("missing")
    except KeyError as exc:
        assert exc.args == ("missing",)
    else:
        raise AssertionError("missing adapter reference must remain observable")
