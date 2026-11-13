"""Evidence is traceable but cannot become an automatic Landscape mutation."""
import pytest

from runtime.aats import Post, Thread
from runtime.evidence_store import EvidenceStore
from runtime.landscape import LandscapeState
from runtime.evidence_landscape_projection import project_store
from runtime.threadrpg_v4_observation import observe_post, record_observation


def sample():
    return Thread("t1").with_post(Post("icchi", "あの子が気になる")).with_post(
        Post("nanashi", "好きなんじゃね？"))


def test_origin_and_references_are_preserved():
    thread = sample()
    store = EvidenceStore()
    store = record_observation(thread, observe_post(thread, 0, origin="human_post"), store)
    store = record_observation(thread, observe_post(
        thread, 1, origin="hypothesis", preceding_refs=(0,)), store)
    assert [e.transition_data["origin"] for e in store.all()] == ["human_post", "hypothesis"]
    assert store.all()[1].transition_data["preceding_refs"] == [0]
    assert store.all()[1].confidence == "unverified"


def test_observation_does_not_mutate_landscape():
    thread = sample()
    store = record_observation(thread, observe_post(thread, 1, origin="joke"), EvidenceStore())
    landscape = LandscapeState.from_snapshot({"existing": "unchanged"})
    project_store(store, landscape)
    assert landscape.snapshot() == {"existing": "unchanged"}
    assert landscape.evidence == []


def test_anonymous_claim_cannot_become_human_fact():
    with pytest.raises(ValueError):
        observe_post(sample(), 1, origin="human_post")


def test_raw_log_mismatch_is_rejected():
    thread = sample()
    obs = observe_post(thread, 1, origin="hypothesis")
    changed = thread.with_post(Post("nanashi", "another"))
    with pytest.raises(ValueError):
        record_observation(Thread("t1", posts=changed.posts[:1]), obs, EvidenceStore())


def test_future_reference_is_rejected():
    with pytest.raises(ValueError):
        observe_post(sample(), 1, origin="joke", preceding_refs=(1,))
