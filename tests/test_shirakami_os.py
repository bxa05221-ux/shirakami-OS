from shirakami_os import ShirakamiOS, example_protocol


def test_minimal_os_boot_execute_and_landscape_round_trip():
    os = ShirakamiOS()

    initial = os.boot({"owner": "human", "state": "ready"})
    result = os.execute(
        "example.landscape.message",
        example_protocol,
        {"message": "hello landscape"},
    )

    assert os.booted is True
    assert initial == {"owner": "human", "state": "ready"}
    assert result.status == "completed"
    assert result.transition.kind == "landscape.message.received"
    assert result.evidence.protocol_id == "example.landscape.message"
    assert result.evidence.transition_data["changed"] is True
    assert result.landscape["owner"] == "human"
    assert result.landscape["message"] == "hello landscape"
