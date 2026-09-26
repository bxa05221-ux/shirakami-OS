import pytest

from runtime.thread_runtime import ThreadRuntime


def test_phase0_replay_preserves_thread_boundary():
    """Replay a representative chat sequence without inferring emotion or authority."""
    runtime = ThreadRuntime()
    events = [runtime.start()]

    replay = [
        ("User", "眠い", "Normal"),
        ("Shirakami", "u_u", "Normal"),
        ("User", "いいよ、ありがと(^_-)", "Normal"),
        ("User", "(￣^￣)ゞ", "Normal"),
        ("User", "(u_u)", "Normal"),
        ("User", "(( _ _ ))..zzzZZ", "Normal"),
        ("User", "いや、お試しだろ？付き合ってんのに。", "Normal"),
        ("User", "♪───Ｏ（≧∇≦）Ｏ────♪", "Normal"),
        ("User", "ヽ(*´∀｀)", "Normal"),
        ("User", "…", "Silence"),
    ]

    for author, content, mode in replay:
        events.append(runtime.append_post(author, content, mode=mode))

    events.append(runtime.transition_mode("CoolDown"))
    events.append(runtime.transition_mode("Normal"))
    events.append(runtime.append_post("User", "了解。", mode="Normal"))
    events.append(runtime.close(reason="replay-complete"))

    assert events[0].kind == "thread.started"
    assert runtime.closed is True
    assert runtime.mode == "Normal"
    assert len(runtime.posts) == len(replay) + 1

    contents = [post.content for post in runtime.posts]
    assert "(u_u)" in contents
    assert "…" in contents
    assert "♪───Ｏ（≧∇≦）Ｏ────♪" in contents

    # AA and silence remain protocol content/state; no psychological inference is attached.
    assert all("emotion" not in post.metadata for post in runtime.posts)
    assert all("authority" not in post.metadata for post in runtime.posts)

    kinds = [event.kind for event in events]
    assert "thread.mode.transitioned" in kinds
    assert "thread.closed" in kinds


def test_phase0_replay_does_not_emit_numeric_heat():
    """The runtime must not invent a numerical emotional/ethical measurement."""
    runtime = ThreadRuntime()
    runtime.start()
    runtime.append_post("User", "…", mode="Silence")

    snapshot = runtime.snapshot()
    assert "heat" not in snapshot
    assert "delta_heat" not in snapshot
    assert "emotion_score" not in snapshot
