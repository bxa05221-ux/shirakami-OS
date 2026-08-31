from src.shirakami.session import SessionStore


def test_session_context_persists_across_turns():
    store = SessionStore()
    assert store.get("s1") == {}
    store.update("s1", {"topic": "OPPAI"})
    assert store.get("s1") == {"topic": "OPPAI"}
    store.update("s1", {"phase": "runtime"})
    assert store.get("s1") == {"topic": "OPPAI", "phase": "runtime"}


def test_sessions_are_isolated():
    store = SessionStore()
    store.update("s1", {"topic": "A"})
    store.update("s2", {"topic": "B"})
    assert store.get("s1") == {"topic": "A"}
    assert store.get("s2") == {"topic": "B"}
