from runtime.http_api import ShirakamiSessionStore


def test_http_api_vertical_slice() -> None:
    store = ShirakamiSessionStore()
    created = store.create("s-http", "landscape-http", {"scene_id": "dogfight"})
    assert created["landscape"]["scene_id"] == "dogfight"

    turn = store.turn("s-http", "歩いてみる")
    assert turn["status"] == "completed"
    assert turn["transition_kind"] == "thread.turn_added"
    assert turn["state"]["turn_count"] == 1
    assert turn["state"]["landscape"]["text"] == "歩いてみる"

    evidence = store.evidence("s-http")
    assert len(evidence) == 1
    assert evidence[0]["transition_kind"] == "thread.turn_added"
