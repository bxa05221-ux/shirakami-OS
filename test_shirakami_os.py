from shirakami_os import ShirakamiOS, example_protocol


def test_minimal_os_boot_and_execute():
    os = ShirakamiOS()

    initial = os.boot({"owner": "human", "state": "ready"})
    result = os.execute(
        "example.landscape.message",
        example_protocol,
        {"message": "hello landscape"},
    )

    assert os.booted is True
    assert initial == {"owner": "human", "state": "ready"}
    assert result.protocol_id == "example.landscape.message"
    assert result.status == "completed"
    assert result.transition.kind == "landscape.message.received"
    assert result.evidence.transition_data["message"] == "hello landscape"
    assert result.landscape["message"] == "hello landscape"


def test_execute_without_explicit_boot_starts_minimal_os():
    os = ShirakamiOS()

    result = os.execute(
        "example.landscape.message",
        example_protocol,
        {"message": "auto boot"},
    )

    assert os.booted is True
    assert result.landscape["message"] == "auto boot"
