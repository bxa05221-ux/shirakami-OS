import pytest

from runtime.thread_runtime import ThreadRuntime


def test_thread_lifecycle_and_post_observation():
    runtime = ThreadRuntime()
    started = runtime.start()

    assert started.kind == "thread.started"
    runtime.append_post("User", "お腹減ったなあ。")
    runtime.append_post("Shirakami", "焼きそば、いいね。")
    runtime.transition_mode("CoolDown")

    assert runtime.mode == "CoolDown"
    assert len(runtime.posts) == 2
    assert runtime.snapshot()["state"] == "active"


def test_aa_is_ordinary_post_content():
    runtime = ThreadRuntime()
    runtime.start()
    runtime.append_post("User", "(u_u)")
    runtime.append_post("User", "♪───Ｏ（≧∇≦）Ｏ────♪")

    assert [p.content for p in runtime.posts] == [
        "(u_u)",
        "♪───Ｏ（≧∇≦）Ｏ────♪",
    ]
    assert all("emotion" not in p.metadata for p in runtime.posts)


def test_soft_silence_can_be_recorded_without_psychological_claim():
    runtime = ThreadRuntime()
    runtime.start()
    runtime.append_post("User", "…", mode="Silence")

    snapshot = runtime.snapshot()
    assert snapshot["mode"] == "Silence"
    assert snapshot["posts"][0]["content"] == "…"


def test_post_limit_closes_thread_but_does_not_create_authority():
    runtime = ThreadRuntime(max_posts=2)
    runtime.start()
    runtime.append_post("User", "one")
    runtime.append_post("Shirakami", "two")

    assert runtime.closed is True
    assert runtime.snapshot()["state"] == "closed"
    assert runtime.snapshot()["post_count"] == 2


def test_invalid_author_and_mode_are_rejected():
    runtime = ThreadRuntime()
    runtime.start()

    with pytest.raises(ValueError):
        runtime.append_post("AI", "invalid")

    with pytest.raises(ValueError):
        runtime.transition_mode("Unknown")


def test_closed_thread_cannot_append():
    runtime = ThreadRuntime(max_posts=1)
    runtime.start()
    runtime.append_post("User", "close")

    with pytest.raises(RuntimeError):
        runtime.append_post("Shirakami", "must fail")
